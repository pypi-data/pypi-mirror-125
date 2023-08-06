use fairvote::{instant_runoff, Voter};

#[test]
fn b_wins_in_third_round() {
    let voter_list = vec![
        vec!["A", "B"],
        vec!["A", "B"],
        vec!["B", "A", "C"],
        vec!["B", "A"],
        vec!["B", "A"],
        vec!["D", "C", "A"],
        vec!["D", "C"],
        vec!["C", "B"],
    ]
    .into_iter()
    .map(Voter::from)
    .collect();

    let winner = instant_runoff(voter_list);
    assert_eq!(winner, Some("B".to_string()));
}

#[test]
fn no_winner_after_3_rounds() {
    let voter_list = vec![
        vec!["A", "B"],
        vec!["A", "B"],
        vec!["B", "A", "C"],
        vec!["B", "A"],
        vec!["B", "A"],
        vec!["D", "C", "A"],
        vec!["D", "C"],
        vec!["C", "A"],
    ]
    .into_iter()
    .map(Voter::from)
    .collect();

    let winner = instant_runoff(voter_list);
    assert_eq!(winner, None);
}
