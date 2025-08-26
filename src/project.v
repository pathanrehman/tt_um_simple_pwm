/*
 * Copyright (c) 2024 Your Name
 * SPDX-License-Identifier: Apache-2.0
 */

`default_nettype none

module tt_um_simple_pwm (
    input  wire [7:0] ui_in,    // Dedicated inputs
    output wire [7:0] uo_out,   // Dedicated outputs
    input  wire [7:0] uio_in,   // IOs: Input path
    output wire [7:0] uio_out,  // IOs: Output path
    output wire [7:0] uio_oe,   // IOs: Enable path (active high: 0=input, 1=output)
    input  wire       ena,      // always 1 when the design is powered, so you can ignore it
    input  wire       clk,      // clock
    input  wire       rst_n     // reset_n - low to reset
);

    // PWM Configuration
    wire [7:0] duty_cycle = ui_in[7:0];  // 8-bit duty cycle input (0-255)
    
    // Internal signals
    reg [7:0] pwm_counter;    // 8-bit counter for PWM generation
    reg pwm_output;           // PWM output signal
    
    // PWM Counter - counts from 0 to 255, then repeats
    always @(posedge clk or negedge rst_n) begin
        if (!rst_n) begin
            pwm_counter <= 8'b0;  // Reset counter to 0
        end else if (ena) begin
            pwm_counter <= pwm_counter + 1;  // Increment counter every clock cycle
        end
    end
    
    // PWM Generation Logic
    always @(posedge clk or negedge rst_n) begin
        if (!rst_n) begin
            pwm_output <= 1'b0;  // Reset PWM output to LOW
        end else if (ena) begin
            if (pwm_counter < duty_cycle)
                pwm_output <= 1'b1;  // Output HIGH when counter < duty_cycle
            else
                pwm_output <= 1'b0;  // Output LOW when counter >= duty_cycle
        end
    end
    
    // Output Assignments
    assign uo_out[0] = pwm_output;        // Main PWM output
    assign uo_out[1] = pwm_counter[0];    // Counter LSB (for debugging)
    assign uo_out[2] = pwm_counter[1];    // Counter bit 1 (for debugging)
    assign uo_out[3] = pwm_counter[2];    // Counter bit 2 (for debugging)
    assign uo_out[4] = pwm_counter[3];    // Counter bit 3 (for debugging)
    assign uo_out[5] = pwm_counter[4];    // Counter bit 4 (for debugging)
    assign uo_out[6] = pwm_counter[5];    // Counter bit 5 (for debugging)
    assign uo_out[7] = pwm_counter[6];    // Counter MSB (for debugging)
    
    // Bidirectional pins - not used, set as inputs
    assign uio_out = 8'b0;
    assign uio_oe = 8'b0;
    
    // List all unused inputs to prevent warnings
    wire _unused = &{uio_in, 1'b0};

endmodule
