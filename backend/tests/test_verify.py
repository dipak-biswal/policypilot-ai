from app.agent.nodes.verify import _is_pure_abstain


def test_abstain_answer_skips_checker():
    assert _is_pure_abstain(
        "The document does not state a maternity waiting period, so I don't know."
    )


def test_answer_with_numbers_still_checked():
    assert not _is_pure_abstain(
        "It doesn't specify maternity, but illness has a 30-day waiting period."
    )


def test_normal_answer_not_abstain():
    assert not _is_pure_abstain("Maternity expenses are excluded [Page 12].")
