use anchor_lang::prelude::*;

declare_id!("9M9j8ToqiNKfDd3sLkekSkZSUGsG6PerrJfuaVeQiBdJ");

#[program]
mod hello_anchor {
    use super::*;
    pub fn initialize(
        ctx: Context<Initialize>,
        row1: [bool; 6],
        row2: [bool; 6],
        row3: [bool; 6],
        row4: [bool; 6],
        row5: [bool; 6],
        row6: [bool; 6],
    ) -> Result<()> {
        ctx.accounts.new_grid.grid[0] = row1;
        ctx.accounts.new_grid.grid[1] = row2;
        ctx.accounts.new_grid.grid[2] = row3;
        ctx.accounts.new_grid.grid[3] = row4;
        ctx.accounts.new_grid.grid[4] = row5;
        ctx.accounts.new_grid.grid[5] = row6;

        msg!("New grid: {:?}!", ctx.accounts.new_grid.grid);
        Ok(())
    }

    pub fn new_turn(ctx: Context<NewTurn>) -> Result<()> {

        let directions: [(i8, i8); 8] = [
            (-1, -1), // above left
            (-1, 0), // above
            (-1, 1), // above right
            (0, 1), // right
            (1, 1), // below right
            (1, 0), // below
            (1, -1), // below left
            (0, -1), // left
        ];

        let new_grid = grid.grid.clone();

        for r in 0..6 {
            for c in 0..6 {

                let mut neighbors: u8 = 0;

                for (x, y) in directions {
                    // check for out of bounds
                    if r + x != -1 && r + x != 6 && c + y != -1 && c + y != 6 {
                        let dx = (r + x) as usize;
                        let dy = (c + y) as usize;
                        if ctx.accounts.grid.grid[dx][dy] == true {
                            neighbors += 1;
                        }
                    }
                }

                let r = r as usize;
                let c = c as usize;

                msg!("Neighbors: {}!", neighbors);                

                if neighbors < 2 {
                    ctx.accounts.grid.grid[r][c] = false;
                }
                if neighbors > 3 && ctx.accounts.grid.grid[r][c] == true {
                    ctx.accounts.grid.grid[r][c] = false;
                }
                if neighbors == 3 && ctx.accounts.grid.grid[r][c] == false {
                    ctx.accounts.grid.grid[r][c] = true;
                }
            }
        }

        msg!("New grid: {:?}!", ctx.accounts.grid.grid);
        Ok(())
    }

    pub fn reset_grid(
        ctx: Context<ResetGrid>,
        row1: [bool; 6],
        row2: [bool; 6],
        row3: [bool; 6],
        row4: [bool; 6],
        row5: [bool; 6],
        row6: [bool; 6],
    ) -> Result<()> {
        ctx.accounts.grid.grid[0] = row1;
        ctx.accounts.grid.grid[1] = row2;
        ctx.accounts.grid.grid[2] = row3;
        ctx.accounts.grid.grid[3] = row4;
        ctx.accounts.grid.grid[4] = row5;
        ctx.accounts.grid.grid[5] = row6;

        msg!("Grid reset to: {:?}!", ctx.accounts.grid.grid);
        Ok(())
    }
}

#[derive(Accounts)]
pub struct Initialize<'info> {
    #[account(
        init, 
        payer = signer, 
        space = 100, // TOOD: MAKE SPACE MORE ACCURATE
        seeds = [b"grid", signer.key().as_ref()], 
        bump
    )]
    pub new_grid: Account<'info, Grid>,
    #[account(mut)]
    pub signer: Signer<'info>,
    pub system_program: Program<'info, System>,
}

#[derive(Accounts)]
pub struct NewTurn<'info> {
    #[account(
        mut,
        seeds = [b"grid", signer.key().as_ref()], 
        bump
    )]
    pub grid: Account<'info, Grid>,
    #[account(mut)]
    pub signer: Signer<'info>,
    pub system_program: Program<'info, System>,
}

#[derive(Accounts)]
pub struct ResetGrid<'info> {
    #[account(
        mut,
        seeds = [b"grid", signer.key().as_ref()],
        bump
    )]
    pub grid: Account<'info, Grid>,
    pub signer: Signer<'info>,
    pub system_program: Program<'info, System>
}

#[account]
pub struct Grid {
    grid: [[bool; 6]; 6],
}
