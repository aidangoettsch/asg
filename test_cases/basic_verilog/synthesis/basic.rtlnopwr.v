/* Verilog module written by vlog2Verilog (qflow) */

module basic(
    input a,
    inout gnd,
    output o,
    inout vdd
);

wire vdd = 1'b1;
wire gnd = 1'b0;

wire a ;
wire o ;
wire _0_ ;

INVX1 _1_ (
    .A(a),
    .Y(_0_)
);

BUFX2 _2_ (
    .A(_0_),
    .Y(o)
);

endmodule
