# SPDX-FileCopyrightText: © 2024 Tiny Tapeout
# SPDX-License-Identifier: Apache-2.0

import cocotb
from cocotb.clock import Clock
from cocotb.triggers import ClockCycles, Timer, RisingEdge

@cocotb.test()
async def test_simple_pwm_basic(dut):
    """Basic functionality test for SimplePWM"""
    
    dut._log.info("Start SimplePWM basic test")
    
    # Set the clock period to 10 us (100 KHz)
    clock = Clock(dut.clk, 10, units="us")
    cocotb.start_soon(clock.start())
    
    # Reset
    dut._log.info("Reset")
    dut.ena.value = 1
    dut.ui_in.value = 0
    dut.uio_in.value = 0
    dut.rst_n.value = 0
    await ClockCycles(dut.clk, 10)
    dut.rst_n.value = 1
    
    dut._log.info("Test SimplePWM behavior")
    
    # Test 1: 0% duty cycle (PWM should be always LOW)
    dut.ui_in.value = 0  # 0% duty cycle
    await ClockCycles(dut.clk, 300)  # Wait more than one complete PWM cycle (256 clocks)
    
    # Check that PWM output is LOW for 0% duty cycle
    pwm_output = dut.uo_out.value & 0x01
    assert pwm_output == 0, f"Expected PWM output LOW for 0% duty cycle, got {pwm_output}"
    dut._log.info("✓ 0% duty cycle test passed")
    
    # Test 2: 100% duty cycle (PWM should be always HIGH after initial cycles)
    dut.ui_in.value = 255  # ~100% duty cycle (255/256)
    await ClockCycles(dut.clk, 300)  # Wait for PWM to stabilize
    
    # Check that PWM output is HIGH for near-100% duty cycle
    pwm_output = dut.uo_out.value & 0x01
    assert pwm_output == 1, f"Expected PWM output HIGH for 100% duty cycle, got {pwm_output}"
    dut._log.info("✓ 100% duty cycle test passed")

@cocotb.test()
async def test_simple_pwm_duty_cycles(dut):
    """Test different duty cycle values"""
    
    dut._log.info("Start duty cycle variation test")
    
    # Set up clock
    clock = Clock(dut.clk, 10, units="us")
    cocotb.start_soon(clock.start())
    
    # Reset
    dut.ena.value = 1
    dut.rst_n.value = 0
    await ClockCycles(dut.clk, 5)
    dut.rst_n.value = 1
    
    # Test different duty cycle values
    test_duty_cycles = [0, 32, 64, 128, 192, 255]
    
    for duty_cycle in test_duty_cycles:
        dut._log.info(f"Testing duty cycle: {duty_cycle}/255 ({duty_cycle/255*100:.1f}%)")
        
        # Set duty cycle
        dut.ui_in.value = duty_cycle
        
        # Wait for a few clock cycles to stabilize
        await ClockCycles(dut.clk, 10)
        
        # Count HIGH and LOW cycles over one complete PWM period (256 clocks)
        high_count = 0
        total_count = 256
        
        for i in range(total_count):
            await RisingEdge(dut.clk)
            pwm_output = dut.uo_out.value & 0x01
            if pwm_output == 1:
                high_count += 1
        
        # Calculate actual duty cycle percentage
        actual_duty_percentage = (high_count / total_count) * 100
        expected_duty_percentage = (duty_cycle / 255) * 100
        
        # Allow some tolerance (±2%) due to timing variations
        tolerance = 2.0
        assert abs(actual_duty_percentage - expected_duty_percentage) <= tolerance, \
            f"Duty cycle mismatch: expected {expected_duty_percentage:.1f}%, got {actual_duty_percentage:.1f}%"
        
        dut._log.info(f"✓ Duty cycle {duty_cycle}: Expected {expected_duty_percentage:.1f}%, Got {actual_duty_percentage:.1f}%")

@cocotb.test()
async def test_simple_pwm_counter(dut):
    """Test PWM counter behavior"""
    
    dut._log.info("Start PWM counter test")
    
    # Set up clock
    clock = Clock(dut.clk, 10, units="us")
    cocotb.start_soon(clock.start())
    
    # Reset
    dut.ena.value = 1
    dut.rst_n.value = 0
    await ClockCycles(dut.clk, 5)
    dut.rst_n.value = 1
    
    # Set a mid-range duty cycle
    dut.ui_in.value = 128  # 50% duty cycle
    
    # Watch counter progression
    await ClockCycles(dut.clk, 2)  # Let counter start
    
    previous_counter = 0
    for i in range(260):  # Slightly more than one full counter cycle
        await RisingEdge(dut.clk)
        
        # Extract counter value from debug outputs (bits 7:1 of uo_out)
        counter_value = (dut.uo_out.value >> 1) & 0x7F  # Get bits [7:1]
        
        # Check counter increments correctly (with rollover)
        expected_counter = (previous_counter + 1) % 128  # 7-bit counter from debug outputs
        
        if i > 5:  # Skip first few cycles for stabilization
            assert counter_value == expected_counter, \
                f"Counter sequence error at cycle {i}: expected {expected_counter}, got {counter_value}"
        
        previous_counter = counter_value
        
        if i == 50:  # Log progress
            dut._log.info(f"Counter at cycle {i}: {counter_value}")
    
    dut._log.info("✓ Counter sequence test passed")

@cocotb.test()
async def test_simple_pwm_enable(dut):
    """Test enable functionality"""
    
    dut._log.info("Start enable functionality test")
    
    # Set up clock
    clock = Clock(dut.clk, 10, units="us")
    cocotb.start_soon(clock.start())
    
    # Reset with enable LOW
    dut.ena.value = 0  # Disable the design
    dut.ui_in.value = 128  # 50% duty cycle
    dut.rst_n.value = 0
    await ClockCycles(dut.clk, 5)
    dut.rst_n.value = 1
    
    # Check that counter doesn't increment when disabled
    await ClockCycles(dut.clk, 10)
    counter_before = (dut.uo_out.value >> 1) & 0x7F
    
    await ClockCycles(dut.clk, 10)
    counter_after = (dut.uo_out.value >> 1) & 0x7F
    
    # Counter should not change when ena=0
    assert counter_before == counter_after, \
        f"Counter changed when disabled: before={counter_before}, after={counter_after}"
    
    dut._log.info("✓ Disable test passed")
    
    # Now enable and check it works
    dut.ena.value = 1  # Enable the design
    await ClockCycles(dut.clk, 20)
    
    # Counter should now be changing
    counter_enabled = (dut.uo_out.value >> 1) & 0x7F
    assert counter_enabled != counter_after, \
        f"Counter not changing when enabled: {counter_enabled}"
    
    dut._log.info("✓ Enable test passed")

@cocotb.test()
async def test_simple_pwm_reset(dut):
    """Test reset functionality"""
    
    dut._log.info("Start reset functionality test")
    
    # Set up clock
    clock = Clock(dut.clk, 10, units="us")
    cocotb.start_soon(clock.start())
    
    # Initial setup
    dut.ena.value = 1
    dut.ui_in.value = 200  # High duty cycle
    dut.rst_n.value = 1
    
    # Let PWM run for a while
    await ClockCycles(dut.clk, 50)
    
    # Apply reset
    dut.rst_n.value = 0
    await ClockCycles(dut.clk, 3)
    
    # Check reset state
    pwm_output = dut.uo_out.value & 0x01
    counter_value = (dut.uo_out.value >> 1) & 0x7F
    
    assert pwm_output == 0, f"PWM output not reset: {pwm_output}"
    assert counter_value == 0, f"Counter not reset: {counter_value}"
    
    dut._log.info("✓ Reset state verified")
    
    # Release reset and verify operation resumes
    dut.rst_n.value = 1
    await ClockCycles(dut.clk, 20)
    
    # Check that PWM is now operating
    new_counter = (dut.uo_out.value >> 1) & 0x7F
    assert new_counter > 0, f"Counter not running after reset release: {new_counter}"
    
    dut._log.info("✓ Reset functionality test passed")
