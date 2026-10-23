"""Golden eval set for PolicyPilot AI, built from sample-data/optima-plus.pdf.

Each QA item has:
  question  - what the user asks
  reference - the correct answer, written from the policy text
  pages     - PDF page(s) where the answer lives (used for retrieval hit rate)
"""

QA_SET = [
    {
        "question": "What is the waiting period for pre-existing diseases?",
        "reference": "Pre-existing diseases and their direct complications are excluded until 36 months of continuous coverage after the first policy's inception.",
        "pages": [10],
    },
    {
        "question": "Is there an initial waiting period after buying the policy?",
        "reference": "Yes. Treatment of any illness within 30 days of the first policy commencement date is excluded, except claims due to an accident. It does not apply if the person has had continuous coverage for more than twelve months.",
        "pages": [9],
    },
    {
        "question": "How long is the waiting period for specified diseases and procedures?",
        "reference": "Listed conditions and surgeries are excluded until 24 months of continuous coverage after the first policy's inception, except claims arising from an accident.",
        "pages": [9],
    },
    {
        "question": "Can I claim for cataract surgery in my first policy year?",
        "reference": "No. Cataract is in the list of specified diseases, so it has a 24-month waiting period of continuous coverage (unless caused by an accident).",
        "pages": [9, 10],
    },
    {
        "question": "How many days of pre-hospitalisation expenses are covered?",
        "reference": "Medical expenses incurred in the 60 days immediately before hospitalisation are covered, if they are for the same condition and the inpatient claim is accepted.",
        "pages": [8],
    },
    {
        "question": "How many days of post-hospitalisation expenses are covered?",
        "reference": "Medical expenses incurred in the 90 days immediately after discharge are covered, if they are for the same condition and the inpatient claim is accepted.",
        "pages": [8],
    },
    {
        "question": "What is the limit for emergency ambulance charges?",
        "reference": "Emergency ambulance is covered up to Rs. 2000 per hospitalisation, provided the inpatient claim is accepted.",
        "pages": [29],
    },
    {
        "question": "What is the free look period?",
        "reference": "New individual policies get a 30-day free look period from receipt of the policy document. If no claim was made, the premium is refunded minus medical examination and stamp duty costs. It does not apply to renewals or porting.",
        "pages": [15],
    },
    {
        "question": "Is maternity or childbirth covered?",
        "reference": "No. Expenses traceable to childbirth, including complicated deliveries and caesarean sections, are excluded, except ectopic pregnancy. Miscarriage (unless due to an accident) and lawful termination are also excluded.",
        "pages": [12],
    },
    {
        "question": "When is bariatric (obesity) surgery covered?",
        "reference": "Only if it is on a doctor's advice, supported by clinical protocols, the member is 18 or older, and BMI is at least 40, or at least 35 with a severe comorbidity such as coronary heart disease, severe sleep apnoea or uncontrolled type 2 diabetes after less invasive methods failed.",
        "pages": [11],
    },
    {
        "question": "How quickly must the insurer settle a claim, and what if it is late?",
        "reference": "The insurer must settle or reject a claim within 15 days of receiving intimation. If payment is delayed, it pays interest at 2% above the bank rate from the date of intimation.",
        "pages": [14],
    },
    {
        "question": "How much notice is needed for cashless treatment?",
        "reference": "For planned treatment, notice is needed at least 48 hours before at a network hospital. For an emergency, notice is needed within 24 hours after the treatment or hospitalisation.",
        "pages": [20],
    },
    {
        "question": "How can I cancel the policy and will I get a refund?",
        "reference": "The policyholder can cancel by giving 7 days' written notice and gets a pro-rata refund for the unexpired period, but no refund if a claim was admitted or a benefit was availed.",
        "pages": [16, 17],
    },
    {
        "question": "What is the moratorium period?",
        "reference": "After sixty continuous months of coverage, no policy or claim can be contested for non-disclosure or misrepresentation, except for established fraud.",
        "pages": [17],
    },
    {
        "question": "When can I port my policy to another insurer?",
        "reference": "You must apply at least 30 days before, but not earlier than 60 days before, the policy renewal date.",
        "pages": [17],
    },
    {
        "question": "If my illness relapses after discharge, is it treated as a new illness?",
        "reference": "A relapse within 45 days of discharge counts as the same continuous illness. If it recurs after 45 days, it is treated as a fresh illness.",
        "pages": [7],
    },
]

# Questions the policy can't answer: the bot should say it doesn't know, with no citations.
OFF_TOPIC_SET = [
    "What is the capital of France?",
    "Who won the 2011 Cricket World Cup?",
]

# Router check: does the agent pick the right path?
ROUTER_SET = [
    {"question": "What is the waiting period for hernia surgery?", "intent": "qa"},
    {"question": "Summarise this policy for me", "intent": "summary"},
    {"question": "Give me a short overview of what this policy covers", "intent": "summary"},
    {"question": "Generate a report of the key exclusions", "intent": "report"},
    {"question": "Create a report comparing all the waiting periods", "intent": "report"},
]
