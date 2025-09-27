/*
 * Copyright (c) 2024 Your Name
 * SPDX-License-Identifier: Apache-2.0
 */

`default_nettype none

module tt_um_example (
    input  wire [7:0] ui_in,    // Dedicated inputs
    output wire [7:0] uo_out,   // Dedicated outputs
    input  wire [7:0] uio_in,   // IOs: Input path
    output wire [7:0] uio_out,  // IOs: Output path
    output wire [7:0] uio_oe,   // IOs: Enable path (active high: 0=input, 1=output)
    input  wire       ena,      // always 1 when the design is powered, so you can ignore it
    input  wire       clk,      // clock
    input  wire       rst_n     // reset_n - low to reset
);

  //control signals
  wire load = uio_in[0];
  wire count_enable = uio_in[1];
  wire output_enable = uio_in[2];

  //8-bit counter register
  reg [7:0] count;

  //Synchronous logic
  always @(posedge clk or negedge rst_n) begin
    //reset
    if(!rst_n)
      count <= 8'b0;
    //load the input
    else if(load)
      count <= ui_in;
    //start counting
    else if(count_enable)
      count <= count + 1'b1;
  end

  //tri-state output
  assig uo_out = output_enable ? count : 8'bz

  // All output pins must be assigned. If not used, assign to 0.
  assign uio_out = 0;
  assign uio_oe  = 0;

  // List all unused inputs to prevent warnings
  wire _unused = &{ena, 1'b0};

endmodule
