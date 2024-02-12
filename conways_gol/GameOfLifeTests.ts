// No imports needed: web3, anchor, pg and more are globally available

describe("Tests", () => {
  const newAccountKp = new web3.Keypair();

  // Grid
  const row1 = [false, true, true, true, false, false];
  const row2 = [false, true, true, true, true, false];
  const row3 = [true, true, false, false, false, false];
  const row4 = [false, false, true, true, false, false];
  const row5 = [false, true, true, true, false, false];
  const row6 = [false, true, true, false, true, false];

  let [grid] = anchor.web3.PublicKey.findProgramAddressSync(
    [Buffer.from("grid"), pg.wallet.publicKey.toBuffer()],
    pg.program.programId
  );

  it("initializeGrid", async () => {
    const tx = await pg.program.methods
      .initialize(row1, row2, row3, row4, row5, row6)
      .accounts({
        newGrid: grid,
        signer: pg.wallet.publicKey,
        systemProgram: web3.SystemProgram.programId,
      })
      .rpc();

    console.log(`New grid created at ${grid.toString()}`);
    console.log(`Use 'solana confirm -v ${tx}' to see the logs`);

    await pg.connection.confirmTransaction(tx);

    const game_account = await pg.program.account.grid.fetch(grid);
    console.log(game_account.grid);
  });

  it("newTurn1", async () => {
    let tx = await pg.program.methods
      .newTurn()
      .accounts({
        grid: grid,
        signer: pg.wallet.publicKey,
        systemProgram: web3.SystemProgram.programId,
      })
      .rpc();

    console.log("New Turn1");
    console.log(`Use 'solana confirm -v ${tx}' to see the logs`);

    await pg.connection.confirmTransaction(tx);

    const game_account = await pg.program.account.grid.fetch(grid);
    console.log(game_account.grid);
  });

  it("newTurn2", async () => {
    let tx = await pg.program.methods
      .newTurn()
      .accounts({
        grid: grid,
        signer: pg.wallet.publicKey,
        systemProgram: web3.SystemProgram.programId,
      })
      .rpc();

    console.log("New Turn2");
    console.log(`Use 'solana confirm -v ${tx}' to see the logs`);

    await pg.connection.confirmTransaction(tx);

    const game_account = await pg.program.account.grid.fetch(grid);
    console.log(game_account.grid);
  });

  it("resetGrid", async () => {
    let tx = await pg.program.methods
      .resetGrid(row1, row2, row3, row4, row5, row6)
      .accounts({
        grid: grid,
        signer: pg.wallet.publicKey,
        systemProgram: web3.SystemProgram.programId,
      })
      .rpc();

    console.log("Reset Grid");
    console.log(`Use 'solana confirm -v ${tx}' to see the logs`);

    await pg.connection.confirmTransaction(tx);

    const game_account = await pg.program.account.grid.fetch(grid);
    console.log(game_account.grid);
  });
});
