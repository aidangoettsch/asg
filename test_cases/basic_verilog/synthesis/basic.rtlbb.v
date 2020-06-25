/* Verilog module written by vlog2Verilog (qflow) */
/* With bit-blasted vectors */
/* With power connections converted to binary 1, 0 */

module basic(
    input a,
    inout gnd,
    output o,
    inout vdd
);

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
