
// No imports needed: web3, anchor, pg and more are globally available

describe("Test Poll Program", async () => {
  // Generate the poll account
  const newPoll = web3.Keypair.generate();

  it("createPoll", async () => {
    // Send transaction
    const txHash = await pg.program.methods
      .create()
      .accounts({
        user: pg.wallet.publicKey,
        poll: newPoll.publicKey,
      })
      .signers([newPoll])
      .rpc();
    console.log(`Use 'solana confirm -v ${txHash}' to see the logs`);

    // Confirm transaction
    await pg.connection.confirmTransaction(txHash);

    // Fetch the created account
    const pollAccount = await pg.program.account.poll.fetch(newPoll.publicKey);

    assert(pollAccount.solana.toString(), "0");
    assert(pollAccount.ethereum.toString(), "0");
    assert(pollAccount.polygone.toString(), "0");
  });

  it("vote", async () => {
    // Send transaction
    const txSolHash = await pg.program.methods
      .vote("sol")
      .accounts({
        user: pg.wallet.publicKey,
        poll: newPoll.publicKey,
      })
      .rpc();

    // Confirm transaction
    await pg.connection.confirmTransaction(txSolHash);

    // Send transaction
    const txEthHash = await pg.program.methods
      .vote("eth")
      .accounts({
        user: pg.wallet.publicKey,
        poll: newPoll.publicKey,
      })
      .rpc();

    // Confirm transaction
    await pg.connection.confirmTransaction(txEthHash);

    // Fetch the poll account
    const pollAccount = await pg.program.account.poll.fetch(newPoll.publicKey);

    console.log("ethereum:", pollAccount.ethereum.toString());
    assert(pollAccount.ethereum.toString(), "1");

    console.log("solana:", pollAccount.solana.toString());
    assert(pollAccount.solana.toString(), "1");

    console.log("polygone:", pollAccount.polygone.toString());
    assert(pollAccount.polygone.toString(), "0");
  });
});

