// No imports needed: web3, anchor, pg and more are globally available

describe("Tests", () => {
    // const newAccountKp = new web3.Keypair();
  
    const userName = "Satoshi";
    const tweetText = "my first tweet";
    const imageLink = "https://upload.wikimedia.org/wikipedia/en/b/b9/Solana_logo.png";
    const tweetID = new anchor.BN(1);
    const tweetIDBuffer = tweetID.toArrayLike(Buffer, 'le', 8); // Convert to little-endian Buffer with a fixed length
  
    const [usersAccount] = anchor.web3.PublicKey.findProgramAddressSync(
      [Buffer.from("user-account"), pg.wallet.publicKey.toBuffer()],
      pg.program.programId
    );
  
    const [tweet] = anchor.web3.PublicKey.findProgramAddressSync(
      [Buffer.from("tweet"), pg.wallet.publicKey.toBuffer(), tweetIDBuffer],
      pg.program.programId
    );
  
    const [like] = anchor.web3.PublicKey.findProgramAddressSync(
      [Buffer.from("like"), pg.wallet.publicKey.toBuffer(), tweetIDBuffer, pg.wallet.publicKey.toBuffer()],
      pg.program.programId
    );
  
    it("initNewUserAccount", async () => {
      const tx = await pg.program.methods
        .createNewUserAccount(userName)
        .accounts({
          owner: pg.wallet.publicKey,
          user: usersAccount,
          systemProgram: web3.SystemProgram.programId,
        })
        .rpc();
  
      await pg.connection.confirmTransaction(tx);
      console.log(`New user account created at ${usersAccount.toString()}`);
      console.log(`Use 'solana confirm -v ${tx}' to see the logs`);
    });
  
    it("createNewTweet", async () => {
      const tx = await pg.program.methods
        .createNewTweet(tweetText, imageLink, tweetID)
        .accounts({
          owner: pg.wallet.publicKey,
          tweets_user_account: usersAccount,
          tweet: tweet,
          systemProgram: web3.SystemProgram.programId,
        })
        .rpc();
  
      await pg.connection.confirmTransaction(tx);
      console.log(`New tweet created at ${tweet.toString()}`);
      console.log(`Use 'solana confirm -v ${tx}' to see the logs`);
    });
  
    it("likeTweet", async () => {
      let tx = await pg.program.methods
        .likeTweet()
        .accounts({
          liker: pg.wallet.publicKey,
          tweet: tweet,
          user: usersAccount,
          like: like,
          systemProgram: web3.SystemProgram.programId,
        })
        .rpc();
  
      await pg.connection.confirmTransaction(tx);
      console.log(`New like was created at ${like.toString()}`);
      console.log(`Use 'solana confirm -v ${tx}' to see the logs`);
    });
  
    it("deleteTweet", async () => {
      let tx = await pg.program.methods
        .deleteTweet()
        .accounts({
          owner: pg.wallet.publicKey,
          tweet: tweet
        })
        .rpc();
  
      await pg.connection.confirmTransaction(tx);
      console.log(
        `Tweet was deleted at ${tweet.toString()}`
      );
      console.log(`Use 'solana confirm -v ${tx}' to see the logs`);
    });
  
  
  });
  