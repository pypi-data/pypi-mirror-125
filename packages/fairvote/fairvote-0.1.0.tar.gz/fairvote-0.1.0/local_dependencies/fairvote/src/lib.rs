#![deny(missing_docs)]

//! Ranked voting algorithms

mod voter;

use std::collections::{HashMap, HashSet};

pub use crate::voter::{VoteRanking, Voter};

type Candidate = String;
/// The outcome of an election.
pub type ElectionOutcome = Option<Candidate>;
type Tally = HashMap<Candidate, usize>;

/// Instant-runoff voting.
///
/// Read more at [https://en.wikipedia.org/wiki/Instant-runoff_voting].
pub fn instant_runoff(mut voter_list: Vec<Voter>) -> ElectionOutcome {
    let mut candidate_list = construct_candidate_list(&voter_list);

    // the theoretically maximum amount of iterations is the amount of candidates in the election
    for _round in 1..=candidate_list.len() {
        let (tally, num_votes) = dbg!(count_votes(&voter_list, &candidate_list));

        // Is there a winner?.
        if let Some(winner) = there_is_a_winner(&tally, num_votes) {
            return Some(winner);
        }

        let mut losers_list = construct_losers_list(&tally);

        // handle case of multiple losers (this also applies to a draw in the last round)
        losers_list = break_tie(losers_list, &voter_list);

        // create next candidate_list, with the losers removed
        let next_candidate_list = candidate_list
            .into_iter()
            .filter(|candidate| !losers_list.contains(candidate))
            .collect::<HashSet<_>>();

        if next_candidate_list.is_empty() {
            // if the next candidate_list will be empty, we just completed the last round. since
            // there was no winner, we return the candidates who survived until the last round
            return None;
        }

        // update candidate_list
        candidate_list = next_candidate_list;

        // advance vote-pointer for voters who voted for dropped candidate(s)
        voter_list
            .iter_mut()
            .for_each(|voter| match voter.current_vote() {
                Some(candidate_name) if losers_list.contains(candidate_name) => voter.advance(),
                _ => (),
            });

        // back to top
    }
    unreachable!("because we return if there is either a winner, or the candidate list is empty")
}

fn construct_candidate_list(voter_list: &[Voter]) -> HashSet<Candidate> {
    voter_list
        .iter()
        .flat_map(|voter| voter.vote_ranking())
        .cloned()
        .collect()
}

fn count_votes(voter_list: &[Voter], candidate_list: &HashSet<Candidate>) -> (Tally, usize) {
    // select current vote for each voter
    let votes = voter_list
        .iter()
        .filter_map(|voter| voter.current_vote())
        .collect::<Vec<_>>();
    // count votes
    let tally = candidate_list
        .iter()
        .map(|candidate_name| {
            let candidate_count = votes.iter().filter(|&&vote| vote == candidate_name).count();
            (candidate_name.to_string(), candidate_count)
        })
        .collect();

    (tally, votes.len())
}

fn there_is_a_winner(tally: &Tally, num_votes: usize) -> Option<Candidate> {
    let potential_winner = tally
        .iter()
        .max_by(|candidate1, candidate2| candidate1.1.cmp(candidate2.1))
        .unwrap();

    // a winner needs 50% + 1 votes of the current votes
    match *potential_winner.1 > (num_votes / 2) {
        true => Some(potential_winner.0.clone()),
        false => None,
    }
}

fn construct_losers_list(tally: &Tally) -> Vec<Candidate> {
    let least_votes = tally.iter().map(|candidate| candidate.1).min().unwrap();

    // filter for all candidates with the least amount of votes
    tally
        .iter()
        .filter(|candidate| candidate.1 == least_votes)
        .map(|candidate| candidate.0.clone())
        .collect()
}

fn break_tie(losers_list: Vec<Candidate>, _voter_list: &[Voter]) -> Vec<Candidate> {
    losers_list
}
