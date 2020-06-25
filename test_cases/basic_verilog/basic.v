module basic (
    input a,
    output o
);
    wire vdd = 1'b1;
    wire gnd = 1'b0;

    assign o =~a;
endmodule
