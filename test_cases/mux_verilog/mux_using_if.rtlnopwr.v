/* Verilog module written by vlog2Verilog (qflow) */

module mux_using_if(
    input din_0,
    input din_1,
    output mux_out,
    input sel
);

wire vdd = 1'b1;
wire gnd = 1'b0;

wire _1_ ;
wire _0_ ;
wire mux_out ;
wire din_0 ;
wire din_1 ;
wire _2_ ;
wire sel ;

NAND2X1 _4_ (
    .A(din_1),
    .B(sel),
    .Y(_1_)
);

BUFX2 _6_ (
    .A(_2_),
    .Y(mux_out)
);

INVX1 _3_ (
    .A(din_0),
    .Y(_0_)
);

OAI21X1 _5_ (
    .A(sel),
    .B(_0_),
    .C(_1_),
    .Y(_2_)
);

endmodule
