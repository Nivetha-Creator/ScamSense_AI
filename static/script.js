const messageInput = document.getElementById("message");
const analyzeBtn = document.getElementById("analyzeBtn");
const clearBtn = document.getElementById("clearBtn");

const resultBox = document.getElementById("result");
const loading = document.getElementById("loading");

const riskResult = document.getElementById("riskResult");
const probability = document.getElementById("probability");
const analysisText = document.getElementById("analysisText");
const aiRiskAssessment =
    document.getElementById("aiRiskAssessment");

const aiWhySuspicious =
    document.getElementById("aiWhySuspicious");

const aiWarningSigns =
    document.getElementById("aiWarningSigns");

const aiSafeSteps =
    document.getElementById("aiSafeSteps");

const riskCard = document.getElementById("riskCard");
const riskIcon = document.getElementById("riskIcon");

const riskSignals = document.getElementById("riskSignals");

const riskScore = document.getElementById("riskScore");
const riskMeter = document.getElementById("riskMeter");
const riskLevel = document.getElementById("riskLevel");

const charCount = document.getElementById("charCount");

const themeToggle = document.getElementById("themeToggle");


// ========================================
// CHARACTER COUNTER
// ========================================

messageInput.addEventListener("input", () => {

    const length = messageInput.value.length;

    charCount.textContent =
        `${length} / 5000`;

});


// ========================================
// CLEAR BUTTON
// ========================================

clearBtn.addEventListener("click", () => {

    messageInput.value = "";

    charCount.textContent =
        "0 / 5000";

    resultBox.classList.add("hidden");

    messageInput.focus();

});


// ========================================
// DARK / LIGHT MODE
// ========================================

const savedTheme =
    localStorage.getItem("scamsense-theme");

if (savedTheme === "dark") {

    document.documentElement.setAttribute(
        "data-theme",
        "dark"
    );

    themeToggle.textContent = "☀️";

}


themeToggle.addEventListener("click", () => {

    const currentTheme =
        document.documentElement.getAttribute(
            "data-theme"
        );


    if (currentTheme === "dark") {

        document.documentElement.removeAttribute(
            "data-theme"
        );

        localStorage.setItem(
            "scamsense-theme",
            "light"
        );

        themeToggle.textContent = "🌙";

    }

    else {

        document.documentElement.setAttribute(
            "data-theme",
            "dark"
        );

        localStorage.setItem(
            "scamsense-theme",
            "dark"
        );

        themeToggle.textContent = "☀️";

    }

});


// ========================================
// WARNING SIGNALS
// ========================================

function displayRiskSignals(signals) {

    riskSignals.innerHTML = "";

    const signalTypes = [

        {
            key: "urgency",
            title: "Urgency or pressure",
            icon: "⏱️"
        },

        {
            key: "money_related",
            title: "Money or payment related",
            icon: "💰"
        },

        {
            key: "credential_requests",
            title: "Sensitive information request",
            icon: "🔐"
        },

        {
            key: "threats",
            title: "Threatening language",
            icon: "⚠️"
        },

        {
            key: "delivery_related",
            title: "Delivery or package related",
            icon: "📦"
        },

        {
            key: "tax_or_fee_related",
            title: "Tax or fee related",
            icon: "🧾"
        },

        {
            key: "links",
            title: "Link detected",
            icon: "🔗"
        }

    ];


    let found = false;


    signalTypes.forEach(signal => {

        const values =
            signals[signal.key] || [];


        if (values.length === 0) {
            return;
        }


        found = true;


        const element =
            document.createElement("div");

        element.className =
            "signal";


        const icon =
            document.createElement("div");

        icon.className =
            "signal-icon";

        icon.textContent =
            signal.icon;


        const content =
            document.createElement("div");

        content.className =
            "signal-content";


        const title =
            document.createElement("strong");

        title.textContent =
            signal.title;


        const details =
            document.createElement("span");

        details.textContent =
            values.join(", ");


        content.appendChild(title);
        content.appendChild(details);

        element.appendChild(icon);
        element.appendChild(content);

        riskSignals.appendChild(element);

    });


    if (!found) {

        riskSignals.innerHTML = `
            <p class="no-signals">
                No specific warning signs were detected.
            </p>
        `;

    }

}


// ========================================
// ANALYZE BUTTON
// ========================================

analyzeBtn.addEventListener(
    "click",
    analyzeMessage
);


// ========================================
// MAIN ANALYSIS FUNCTION
// ========================================
function displayAIAnalysis(text) {

    aiRiskAssessment.textContent =
        extractSection(
            text,
            "RISK ASSESSMENT:",
            "WHY IT MAY BE SUSPICIOUS:"
        );

    aiWhySuspicious.textContent =
        extractSection(
            text,
            "WHY IT MAY BE SUSPICIOUS:",
            "WARNING SIGNS:"
        );

    aiWarningSigns.textContent =
        extractSection(
            text,
            "WARNING SIGNS:",
            "SAFE NEXT STEPS:"
        );

    aiSafeSteps.textContent =
        extractSection(
            text,
            "SAFE NEXT STEPS:",
            null
        );
}


function extractSection(
    text,
    startMarker,
    endMarker
) {

    const start =
        text.indexOf(startMarker);


    if (start === -1) {
        return "No information provided.";
    }


    const contentStart =
        start + startMarker.length;


    let contentEnd =
        text.length;


    if (endMarker) {

        const end =
            text.indexOf(
                endMarker,
                contentStart
            );

        if (end !== -1) {
            contentEnd = end;
        }

    }


    return text
        .substring(
            contentStart,
            contentEnd
        )
        .trim();

}
async function analyzeMessage() {

    const message =
        messageInput.value.trim();


    if (!message) {

        alert(
            "Please enter a message to analyze."
        );

        messageInput.focus();

        return;

    }


    // Show loading

    loading.classList.remove("hidden");

    resultBox.classList.add("hidden");

    analyzeBtn.disabled = true;


    try {

        const response =
            await fetch(
                "/analyze",
                {
                    method: "POST",

                    headers: {
                        "Content-Type":
                            "application/json"
                    },

                    body: JSON.stringify({
                        message: message
                    })
                }
            );


        const data =
            await response.json();


        if (!response.ok) {

            throw new Error(
                data.error ||
                "Unable to analyze the message."
            );

        }


        // ====================================
        // ML RESULT
        // ====================================

        const result =
            data.ml_result.result;


        const probabilityValue =
            data.ml_result.scam_probability;


        riskResult.textContent =
            result;


        probability.textContent =
            `ML scam probability: ${probabilityValue}%`;


        // ====================================
        // RISK SCORE
        // ====================================

        const riskScoreValue =
            data.ml_result.risk_score;


        const riskLevelValue =
            data.ml_result.risk_level;


        riskScore.textContent =
            `${riskScoreValue} / 100`;


        riskMeter.style.width =
            `${riskScoreValue}%`;


        riskLevel.textContent =
            `Risk Level: ${riskLevelValue}`;


        // ====================================
        // RISK CARD APPEARANCE
        // ====================================

        riskCard.classList.remove(
            "risk-safe",
            "risk-danger"
        );


        if (riskLevelValue === "HIGH") {

            riskIcon.textContent = "⚠️";

            riskResult.style.color =
                "var(--danger)";

        }

        else if (riskLevelValue === "MEDIUM") {

            riskIcon.textContent = "⚠️";

            riskResult.style.color =
                "var(--warning)";

        }

        else {

            riskIcon.textContent = "✓";

            riskResult.style.color =
                "var(--success)";

        }


        // ====================================
        // WARNING SIGNS
        // ====================================

        displayRiskSignals(
            data.ml_result.risk_signals
        );


        // ====================================
        // AI ANALYSIS
        // ====================================

        analysisText.textContent =
            data.analysis ||
            "No additional AI analysis was returned.";


        // ====================================
        // SHOW RESULT
        // ====================================

        resultBox.classList.remove(
            "hidden"
        );


        resultBox.scrollIntoView({
            behavior: "smooth",
            block: "start"
        });


    }

    catch (error) {

        console.error(error);

        alert(
            "Something went wrong while analyzing the message.\n\n" +
            error.message
        );

    }

    finally {

        loading.classList.add("hidden");

        analyzeBtn.disabled = false;

    }

}