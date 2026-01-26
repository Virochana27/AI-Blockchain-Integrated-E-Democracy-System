/* =========================
   VOTING UX SCRIPT
========================= */

/*
 This script handles:
 - Client-side confirmation before voting
 - Disable double submission
 - Simple UX feedback

 Backend responsibility:
 - Vote validation
 - One-person-one-vote enforcement
 - Blockchain ledger entry
*/


/* -------------------------
   Confirm Vote Submission
------------------------- */

function confirmVoteSubmission() {
    return confirm(
        "Are you sure you want to submit your vote?\n" +
        "Once submitted, the vote cannot be changed."
    );
}


/* -------------------------
   Disable Double Submit
------------------------- */

document.addEventListener("DOMContentLoaded", () => {
    const voteForm = document.getElementById("vote-form");

    if (!voteForm) return;

    voteForm.addEventListener("submit", (event) => {
        if (!confirmVoteSubmission()) {
            event.preventDefault();
            return;
        }

        const submitBtn = voteForm.querySelector("button[type='submit']");
        if (submitBtn) {
            submitBtn.disabled = true;
            submitBtn.innerText = "Submitting...";
        }
    });
});
