use fairvote::{ElectionOutcome, VoteRanking, Voter};
use pyo3::prelude::*;

/// Instant-runoff voting.
///
/// Accepts a list of ranked lists of candidates. Returns one candidate or `None`.
#[pyfunction]
#[pyo3(text_signature = "(vote_ranking_list: List[List[str]]) -> Optional[str]")]
fn instant_runoff(vote_ranking_list: Vec<VoteRanking>) -> PyResult<ElectionOutcome> {
    let voter_list = Voter::new_list(vote_ranking_list);
    Ok(fairvote::instant_runoff(voter_list))
}

/// A Python module implemented in Rust. The name of this function must match
/// the `lib.name` setting in the `Cargo.toml`, else Python will not be able to
/// import the module.
#[pymodule]
fn fairvote(_py: Python, m: &PyModule) -> PyResult<()> {
    m.add_function(wrap_pyfunction!(instant_runoff, m)?)?;

    Ok(())
}
