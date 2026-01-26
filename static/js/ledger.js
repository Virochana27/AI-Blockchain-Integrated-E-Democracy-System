/* =========================
   LEDGER EXPLORER SCRIPT
========================= */

/*
 This script handles:
 - Client-side validation for hash input
 - Copy transaction ID to clipboard
 - UX feedback

 Backend responsibility:
 - Ledger verification
 - Data integrity
*/


/* -------------------------
   Validate Hash Input
------------------------- */

function validateLedgerSearch() {
    const input = document.getElementById("ledger-hash-input");

    if (!input) return true;

    const value = input.value.trim();

    if (value.length < 10) {
        alert("Please enter a valid transaction ID or hash.");
        return false;
    }

    return true;
}


/* -------------------------
   Copy to Clipboard
------------------------- */

function copyToClipboard(text) {
    if (!navigator.clipboard) {
        alert("Clipboard not supported");
        return;
    }

    navigator.clipboard.writeText(text)
        .then(() => {
            alert("Copied to clipboard");
        })
        .catch(() => {
            alert("Unable to copy");
        });
}


/* -------------------------
   Attach Events
------------------------- */

document.addEventListener("DOMContentLoaded", () => {
    const form = document.getElementById("ledger-search-form");

    if (form) {
        form.addEventListener("submit", (e) => {
            if (!validateLedgerSearch()) {
                e.preventDefault();
            }
        });
    }
});
