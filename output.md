# Components
- NAND2X1 at (110, 20)
- BUFX2 at (110, 50)
- INVX1 at (50, 20)
- OAI21X1 at (80, 20)
- Input din_0 at (20, 20)
- Input din_1 at (20, 50)
- Output mux_out at (140, 20)
- Input sel at (20, 80)

# Lines
- Line from NAND2X1 at (110, 20) pin #1 to OAI21X1 at (80, 20) pin #5
- Line from Input din_1 at (20, 50) pin #0 to NAND2X1 at (110, 20) pin #3
- Line from OAI21X1 at (80, 20) pin #2 to NAND2X1 at (110, 20) pin #4
- Line from Input sel at (20, 80) pin #0 to NAND2X1 at (110, 20) pin #4
- Line from Input sel at (20, 80) pin #0 to OAI21X1 at (80, 20) pin #2
- Line from OAI21X1 at (80, 20) pin #4 to BUFX2 at (110, 50) pin #2
- Line from BUFX2 at (110, 50) pin #3 to Output mux_out at (140, 20) pin #0
- Line from Input din_0 at (20, 20) pin #0 to INVX1 at (50, 20) pin #0
- Line from INVX1 at (50, 20) pin #1 to OAI21X1 at (80, 20) pin #3
