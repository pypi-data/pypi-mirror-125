use std::collections::HashSet;

use crate::Candidate;

/// List of [`Candidate`]s in order of ranking
pub type VoteRanking = Vec<Candidate>;

/// The voting list of one individual voter
#[derive(Clone, Debug)]
pub struct Voter {
    /// List of [`Candidate`]s in order of ranking
    vote_ranking: VoteRanking,
    /// Pointer to currently relevant vote
    vote_pointer: usize,
}

impl Voter {
    /// Create a new voter, based on a [`VoteRanking`]
    pub fn new(vote_ranking: VoteRanking) -> Self {
        assert_eq!(
            vote_ranking.len(),
            // transforming into a HashSet will remove duplicates
            vote_ranking.iter().collect::<HashSet<_>>().len(),
            "vote_ranking contains duplicate votes, which is not allowed!"
        );

        Self {
            vote_ranking,
            vote_pointer: 0,
        }
    }

    /// Create list of [`Voter`]s, based on list of [`VoteRanking`]s
    pub fn new_list(vote_ranking_list: Vec<VoteRanking>) -> Vec<Self> {
        vote_ranking_list.into_iter().map(Voter::new).collect()
    }

    /// Increment `vote_pointer` by one
    pub(crate) fn advance(&mut self) {
        self.vote_pointer += 1;
    }

    /// The first [`Candidate`] of this voter, which didn't get eliminated yet
    pub(crate) fn current_vote(&self) -> Option<&Candidate> {
        self.vote_ranking.get(self.vote_pointer)
    }

    /// The number of votes
    #[cfg(test)]
    pub(crate) fn len(&self) -> usize {
        self.vote_ranking.len()
    }

    /// List of [`Candidate`]s in order of ranking
    pub(crate) fn vote_ranking(&self) -> &VoteRanking {
        &self.vote_ranking
    }
}

impl From<Vec<&str>> for Voter {
    fn from(vote_ranking: Vec<&str>) -> Self {
        Self::new(vote_ranking.iter().map(|c| c.to_string()).collect())
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn advance_out_of_bounds() {
        let mut voter = Voter::from(vec!["A", "B", "C"]);

        // advance to maximum value
        for _ in 0..(voter.len() - 1) {
            voter.advance();
        }
        // advance one element too far
        voter.advance();
        // therefore the current vote should be None
        assert_eq!(voter.current_vote(), None);
    }

    #[test]
    #[should_panic]
    fn duplicate_votes() {
        Voter::from(vec!["A", "B", "B"]);
    }

    #[test]
    fn empty_votes() {
        Voter::from(vec![]);
    }
}
