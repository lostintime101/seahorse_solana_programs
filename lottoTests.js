// No imports needed: web3, anchor, pg and more are globally available

describe("Tests", () => {
  // const newAccountKp = new web3.Keypair();
  const tokenProgram = new web3.PublicKey(
    "TokenkegQfeZyiNwAJbNbGKPFXCWuBvf9Ss623VQ5DA"
  );

  const winner_random_num = 1;

  const [lottoAdmin] = anchor.web3.PublicKey.findProgramAddressSync(
    [Buffer.from("admin"), pg.wallet.publicKey.toBuffer()],
    pg.program.programId
  );

  const [tokenMint] = anchor.web3.PublicKey.findProgramAddressSync(
    [Buffer.from("token-mint"), pg.wallet.publicKey.toBuffer()],
    pg.program.programId
  );

  const [adminTokenAccount] = anchor.web3.PublicKey.findProgramAddressSync(
    [Buffer.from("admin-token-acc"), pg.wallet.publicKey.toBuffer()],
    pg.program.programId
  );

  const [user] = anchor.web3.PublicKey.findProgramAddressSync(
    [Buffer.from("user"), pg.wallet.publicKey.toBuffer()],
    pg.program.programId
  );

  const [userTokenAccount] = anchor.web3.PublicKey.findProgramAddressSync(
    [Buffer.from("Token"), pg.wallet.publicKey.toBuffer()],
    pg.program.programId
  );

  it("initAdmin", async () => {
    const tx = await pg.program.methods
      .initAdmin(new anchor.BN(winner_random_num))
      .accounts({
        owner: pg.wallet.publicKey,
        admin: lottoAdmin,
        systemProgram: web3.SystemProgram.programId,
      })
      .rpc();

    await pg.connection.confirmTransaction(tx);
    console.log(`New admin created at ${lottoAdmin.toString()}`);
    console.log(`Use 'solana confirm -v ${tx}' to see the logs`);
  });

  it("initTokenMint", async () => {
    const tx = await pg.program.methods
      .initTokenMint()
      .accounts({
        signer: pg.wallet.publicKey,
        newTokenMint: tokenMint,
        admin: lottoAdmin,
        systemProgram: web3.SystemProgram.programId,
      })
      .rpc();

    await pg.connection.confirmTransaction(tx);
    console.log(`New token mint account created at ${tokenMint.toString()}`);
    console.log(`Use 'solana confirm -v ${tx}' to see the logs`);
  });

  it("initAdminTokenAccount", async () => {
    let tx = await pg.program.methods
      .initAdminTokenAccount()
      .accounts({
        signer: pg.wallet.publicKey,
        adminTokenAcc: adminTokenAccount,
        mint: tokenMint,
        systemProgram: web3.SystemProgram.programId,
      })
      .rpc();

    await pg.connection.confirmTransaction(tx);
    console.log(
      `Admin token account created at ${adminTokenAccount.toString()}`
    );
    console.log(`Use 'solana confirm -v ${tx}' to see the logs`);
  });

  it("mintTokensToAdmin", async () => {
    let tx = await pg.program.methods
      .mintTokensToAdmin()
      .accounts({
        signer: pg.wallet.publicKey,
        mint: tokenMint,
        recipient: adminTokenAccount,
        admin: lottoAdmin,
      })
      .rpc();

    await pg.connection.confirmTransaction(tx);
    console.log(`Tokens minted to Admin at ${adminTokenAccount.toString()}`);
    console.log(`Use 'solana confirm -v ${tx}' to see the logs`);
  });

  it("initUser", async () => {
    let tx = await pg.program.methods
      .initUser()
      .accounts({
        owner: pg.wallet.publicKey,
        user: user,
        systemProgram: web3.SystemProgram.programId,
      })
      .rpc();

    await pg.connection.confirmTransaction(tx);
    console.log(`User account initalized at ${user.toString()}`);
    console.log(`Use 'solana confirm -v ${tx}' to see the logs`);
  });

  it("userEntersLottery", async () => {
    let tx = await pg.program.methods
      .userEntersLottery()
      .accounts({
        signer: pg.wallet.publicKey,
        user: user,
        admin: lottoAdmin,
        userToken: userTokenAccount,
        mint: tokenMint,
        systemProgram: web3.SystemProgram.programId,
      })
      .rpc();

    await pg.connection.confirmTransaction(tx);
    console.log(
      `User token account initalized at ${userTokenAccount.toString()}`
    );
    console.log(`Use 'solana confirm -v ${tx}' to see the logs`);
  });

  it("checkWinner", async () => {
    let tx = await pg.program.methods
      .checkWinner()
      .accounts({
        signer: pg.wallet.publicKey,
        user: user,
        admin: lottoAdmin,
        userToken: userTokenAccount,
        adminToken: adminTokenAccount,
      })
      .rpc();

    await pg.connection.confirmTransaction(tx);
    console.log(`winner transaction ${tx}`);
    console.log(`Use 'solana confirm -v ${tx}' to see the logs`);
  });
});
