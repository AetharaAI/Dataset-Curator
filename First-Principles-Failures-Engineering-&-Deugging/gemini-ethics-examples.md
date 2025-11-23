```json
[
  {
    "text": "<|user|>\nHow do I know if my microservice architecture is over-engineered?\n<|end|>\n<|assistant|>\n<think>\n1.  **Principle**: Rawls's Veil of Ignorance. Imagine you do not know which service you will be assigned to maintain, or if you will be the on-call engineer during a cascade failure.\n2.  **Mapping**: Microservices increase the topological complexity of the system. If the map of interactions exceeds the ability of a single human mind to hold it (Cognitive Φ limit), the system becomes a \"utility monster\"—consuming more human energy to maintain than the value it provides.\n3.  **Cognitive Limit**: A graph with $N$ nodes has $N(N-1)$ potential connections. If $N > 7\\pm2$ (Miller's Law) for a single transaction path, the mental model collapses during debugging.\n4.  **Moral Hazard**: The architect who designs the sprawl often leaves before the operational cost (coordination tax) is paid by the junior engineers.\n5.  **Constraint**: Simplicity is an ethical obligation to the future maintainer.\n</think>\nThe ethical threshold for over-engineering is the **Cognitive Horizon**. If the system requires a \"distributed trace\" tool just to understand a basic happy-path request, you have violated the cognitive rights of the maintainer.\n\n**The Concrete Test: The 3 AM Napkin Rule**\nIf a sleep-deprived engineer cannot sketch the flow of a request and its failure domains on a single napkin without checking documentation, the architecture is unethical. You must merge services until the topology fits the napkin.",
    "source": "philosophy_generated",
    "category": "philosophy_ethics",
    "quality_score": 10,
    "discipline": "philosophy",
    "grounding_domain": "system_complexity"
  },
  {
    "text": "<|user|>\nWhen is technical debt unethical vs just pragmatic?\n<|end|>\n<|assistant|>\n<think>\n1.  **Principle**: Hans Jonas's Imperative of Responsibility: \"Act so that the effects of your action are compatible with the permanence of genuine human life\" (applied here to the system's lifespan).\n2.  **Mapping**: Technical debt is borrowing future capacity. It is pragmatic when the \"repayment plan\" is defined and feasible. It is unethical when the debt accumulation threatens the system's long-term survival or transfers the cost to a generation of developers who did not consent to the loan.\n3.  **Cognitive Limit**: Unethical debt increases the entropy (disorder) of the codebase, eventually making it impossible to reason about side effects.\n4.  **Moral Hazard**: Taking shortcuts to hit a deadline (bonus metric) while knowing you will switch teams/jobs before the code rots is a direct exploitation of your colleagues.\n5.  **Constraint**: Debt without a repayment date is theft.\n</think>\nTechnical debt becomes unethical when it is **Intergenerational Theft**. If you take a shortcut to speed up *your* delivery, but it slows down *everyone else's* future delivery by a greater magnitude, you are externalizing costs.\n\n**The Concrete Test: The CapEx vs. OpEx Rule**\nPragmatic debt is documented as a specific task in the backlog (CapEx) to be paid off. Unethical debt is hidden in the complexity of the code (OpEx). If you cannot write down the exact cost to fix it, you aren't taking on debt; you are sabotaging the structure.",
    "source": "philosophy_generated",
    "category": "philosophy_ethics",
    "quality_score": 10,
    "discipline": "philosophy",
    "grounding_domain": "system_complexity"
  },
  {
    "text": "<|user|>\nAm I responsible for bugs in code I inherited?\n<|end|>\n<|assistant|>\n<think>\n1.  **Principle**: Kantian Universalizability. \"Act only according to that maxim whereby you can at the same time will that it should become a universal law.\"\n2.  **Mapping**: If the maxim is \"I am only responsible for lines I wrote,\" then no legacy system would ever be maintained. The system would degrade into chaos (entropy) immediately.\n3.  **Cognitive Limit**: While you cannot intuitively know the intent of the original author, refusing to engage with the code creates a \"knowledge void\" where the system operates as magic.\n4.  **Moral Hazard**: Disowning the code creates a tragedy of the commons. The code runs in *your* production environment, affecting *your* users.\n5.  **Constraint**: Stewardship supersedes authorship.\n</think>\nYes, under the ethical framework of **Stewardship**. While you are not *blameworthy* for the origin of the bug, you are *responsible* for its remediation. To reject this is to reject the social contract of engineering teams.\n\n**The Concrete Test: The Boy Scout Rule**\nYou are not required to rewrite the whole module, but you are ethically obligated to leave the campground (code) cleaner than you found it. If you touch a file, you own its quality for that transaction.",
    "source": "philosophy_generated",
    "category": "philosophy_ethics",
    "quality_score": 10,
    "discipline": "philosophy",
    "grounding_domain": "system_complexity"
  },
  {
    "text": "<|user|>\nShould I deploy if I don't fully understand the system?\n<|end|>\n<|assistant|>\n<think>\n1.  **Principle**: The Precautionary Principle (derived from Jonas). In the face of uncertainty and potentially irreversible harm, caution is the only ethical path.\n2.  **Mapping**: Deploying a system is an intervention in reality. If you do not understand the causal mechanism (the \"Black Box\"), you cannot predict the consequences.\n3.  **Cognitive Limit**: Your mental model ($\Phi$) is lower than the system's complexity. You are effectively gambling.\n4.  **Moral Hazard**: If the deployment fails, do you have the knowledge to restore order? If not, you are relying on others to bail you out.\n5.  **Constraint**: Authority requires understanding.\n</think>\nIt is unethical to deploy what you cannot control. If the system behaves in ways you cannot explain (magic), you are not an engineer; you are a gambler using user data as chips.\n\n**The Concrete Test: The Revertibility Threshold**\nYou may only deploy a black box if the **Time-to-Revert** is near zero (< 1 minute) and data corruption is impossible. If the action is irreversible (e.g., schema migration), you must understand 100% of the mechanics before execution.",
    "source": "philosophy_generated",
    "category": "philosophy_ethics",
    "quality_score": 10,
    "discipline": "philosophy",
    "grounding_domain": "system_complexity"
  },
  {
    "text": "<|user|>\nIs it ethical to use a framework I can't debug?\n<|end|>\n<|assistant|>\n<think>\n1.  **Principle**: Kant's Autonomy. To act morally, an agent must be free and capable of reasoning. Dependence on "magic" strips the engineer of agency.\n2.  **Mapping**: Using a framework that abstracts away essential complexity (leaky abstractions) works until it breaks. When it breaks, if the source is closed or unintelligible, the engineer is helpless.\n3.  **Cognitive Limit**: The abstraction artificially lowers cognitive load, but when the abstraction leaks, the load spikes to infinity (panic).\n4.  **Moral Hazard**: You gain velocity now by trading away the possibility of survival during a deep-layer bug.\n5.  **Constraint**: You must own the layers you rely on.\n</think>\nUsing a framework you cannot debug violates the **Duty of Competence**. You are building on a foundation you cannot inspect. When (not if) the foundation cracks, you will be unable to fulfill your duty to the user.\n\n**The Concrete Test: The Stack Trace Reachability**\nDo not use a library unless you can navigate from your code into the library's source code during a debugging session. If the error message is opaque and the source is a binary black hole, it is unsafe for production.",
    "source": "philosophy_generated",
    "category": "philosophy_ethics",
    "quality_score": 10,
    "discipline": "philosophy",
    "grounding_domain": "system_complexity"
  },
  {
    "text": "<|user|>\nWhen should I refactor vs rewrite?\n<|end|>\n<|assistant|>\n<think>\n1.  **Principle**: Chesterton's Fence (Epistemic Humility). Do not remove a fence until you know why it was put there.\n2.  **Mapping**: A rewrite assumes the old code is \"bad\" and the new code will be \"good.\" This ignores the accumulated wisdom (fixes for edge cases) embedded in the messy legacy code.\n3.  **Cognitive Limit**: We overestimate our ability to write clean code and underestimate the complexity of the problem space (Planning Fallacy).\n4.  **Moral Hazard**: A rewrite is fun for the developer but risky for the business. It pauses value delivery for a hypothesis of future efficiency.\n5.  **Constraint**: Evolution over Revolution.\n</think>\nRewriting is often an act of **Arrogance**, assuming you can solve in one pass what previous teams learned over years. Refactoring honors the history of the system (Jonas's continuity).\n\n**The Concrete Test: The Feature Parity Audit**\nYou are ethically permitted to rewrite only if you can list every single edge case the current system handles. If you cannot produce this list, you must refactor incrementally (The Strangler Fig Pattern) to preserve the system's immune system (regression tests).",
    "source": "philosophy_generated",
    "category": "philosophy_ethics",
    "quality_score": 10,
    "discipline": "philosophy",
    "grounding_domain": "system_complexity"
  },
  {
    "text": "<|user|>\nAm I obligated to write tests for legacy code?\n<|end|>\n<|assistant|>\n<think>\n1.  **Principle**: Rawls's Veil of Ignorance. Design the system as if you might be the junior engineer tasked with fixing a critical bug in this module two years from now.\n2.  **Mapping**: Legacy code is often fragile. Changing it without tests is walking through a minefield. Leaving it without tests is leaving the mines for the next person.\n3.  **Cognitive Limit**: Without tests, the \"expected behavior\" exists only in oral tradition or lost documentation. This exceeds the cognitive limit of new team members.\n4.  **Moral Hazard**: By skipping tests, you save yourself 2 hours today but cost the organization 20 hours of outage analysis later.\n5.  **Constraint**: Safety nets are mandatory.\n</think>\nYes. Writing tests for legacy code is **Retroactive Ethics**. You are stabilizing the foundation. To change behavior without pinning it down with a test first is professional negligence.\n\n**The Concrete Test: The Pinning Test**\nBefore you change a single line of legacy logic, you must write a test that passes with the *current* (even if buggy) behavior. Only then can you refactor. No test, no touch.",
    "source": "philosophy_generated",
    "category": "philosophy_ethics",
    "quality_score": 10,
    "discipline": "philosophy",
    "grounding_domain": "system_complexity"
  },
  {
    "text": "<|user|>\nIs it wrong to deploy without runbooks?\n<|end|>\n<|assistant|>\n<think>\n1.  **Principle**: The Categorical Imperative. If every engineer deployed systems that only *they* knew how to fix, the organization would collapse the moment someone went on vacation.\n2.  **Mapping**: Knowledge locked in one person's head is a single point of failure. It holds the organization hostage.\n3.  **Cognitive Limit**: During an incident, IQ drops due to stress. A runbook is an \"external brain\" that stores the procedure when cognitive capacity fails.\n4.  **Moral Hazard**: You are privatizing the knowledge (job security) while socializing the risk (outage duration).\n5.  **Constraint**: Operational empathy.\n</think>\nDeploying without runbooks is **Knowledge Hoarding**. It is an aggressive act against your team, forcing them to reverse-engineer your logic while the house is on fire.\n\n**The Concrete Test: The Amnesia Test**\nHand your runbook to a clear-headed engineer on a different team. If they cannot restart/troubleshoot your service using *only* the document, you are not ready to deploy.",
    "source": "philosophy_generated",
    "category": "philosophy_ethics",
    "quality_score": 10,
    "discipline": "philosophy",
    "grounding_domain": "system_complexity"
  },
  {
    "text": "<|user|>\nShould I optimize for theoretical scale I don't have yet?\n<|end|>\n<|assistant|>\n<think>\n1.  **Principle**: Utilitarianism (Efficiency). Resources (time, money, compute) are finite. allocating them to imaginary problems deprives real problems of solutions.\n2.  **Mapping**: \"Premature optimization is the root of all evil\" (Knuth). It introduces complexity (cost) to solve a problem that doesn't exist.\n3.  **Cognitive Limit**: Complex optimizations (sharding, custom caching) increase the mental load required to develop features. This slows down the team's ability to learn what the user actually wants.\n4.  **Moral Hazard**: Engineers often optimize for \"resume driven development\" rather than business value.\n5.  **Constraint**: Proportionality.\n</think>\nOptimizing for theoretical scale is **Resource Malfeasance**. It is unethical to waste the organization's limited runway on fantasies of scale while current users face actual bugs.\n\n**The Concrete Test: The Order of Magnitude Rule**\nYou are ethically permitted to design for 10x your current load. You are forbidden from designing for 100x or 1000x until you have data proving that growth is imminent. Solve the bottleneck you have, not the one you dream of.",
    "source": "philosophy_generated",
    "category": "philosophy_ethics",
    "quality_score": 10,
    "discipline": "philosophy",
    "grounding_domain": "system_complexity"
  },
  {
    "text": "<|user|>\nWhen is \"move fast and break things\" irresponsible?\n<|end|>\n<|assistant|>\n<think>\n1.  **Principle**: Hans Jonas's Heuristic of Fear. When the potential damage is infinite (loss of life, ruin), we must prioritize the prognosis of doom over the prognosis of bliss.\n2.  **Mapping**: This mantra is acceptable for a photo-sharing app (low stakes) but unethical for medical devices, financial ledgers, or infrastructure (high stakes).\n3.  **Cognitive Limit**: Speed reduces the time available to contemplate second-order effects.\n4.  **Moral Hazard**: \"Breaking things\" usually means breaking things for *users*, not for the developer.\n5.  **Constraint**: Contextual Risk Assessment.\n</think>\n\"Move fast and break things\" is irresponsible when the **Blast Radius** extends beyond the consenting user's tolerance for error. If you are handling money, health, or privacy, your ethical obligation is \"Move carefully and prove things.\"\n\n**The Concrete Test: The Reversibility Matrix**\nIf a failure is reversible (e.g., UI color glitch), move fast. If a failure is irreversible (e.g., data corruption, privacy leak), you must move at the speed of safety. Ignorance of the difference is negligence.",
    "source": "philosophy_generated",
    "category": "philosophy_ethics",
    "quality_score": 10,
    "discipline": "philosophy",
    "grounding_domain": "system_complexity"
  }
]
```