import random
from typing import List, Tuple

def generate_noir_tropes(subversion_percentage: float = 0.3, num_tropes: int = 10) -> List[Tuple[str, str, str]]:
    """
    Generate a list of noir tropes with their implementations.
    
    Args:
        subversion_percentage: Probability of using a subversion instead of convention (0.0 to 1.0)
        num_tropes: Number of tropes to generate
    
    Returns:
        List of tuples containing (trope_name, implementation_type, implementation_description)
    """
    
    # Complete revised tropes data
    tropes_data = {
        1: {
            'title': 'The False MacGuffin Reveal',
            'convention': 'The precious object driving all motivations is revealed as worthless, teaching that human greed creates value where none exists.',
            'subversions': [
                'The Personal MacGuffin: The object is worthless to everyone except the protagonist, for whom it holds irreplaceable sentimental value—revealing that worth is entirely subjective',
                'The MacGuffin\'s True Cost: The object is valuable, but obtaining it required destroying something even more precious that the characters only realize afterward',
                'The Symbolic MacGuffin: The object\'s material worth is irrelevant; its true value lies in what possessing it represents about power, status, or identity',
                'The MacGuffin Network: The object is one piece of a larger collection—worthless alone but incredibly valuable as part of a set that no one character can complete',
                'The Temporal MacGuffin: The object\'s value fluctuates based on when it\'s discovered—it was priceless yesterday, worthless today, but will be invaluable tomorrow'
            ]
        },
        2: {
            'title': 'The Femme Fatale\'s True Nature',
            'convention': 'The seductive woman reveals she was manipulating the protagonist all along, never truly loved him, and likely attempts to kill or abandon him.',
            'subversions': [
                'The Defensive Femme Fatale: She manipulates men because she\'s learned it\'s the only way to survive in a predatory world—her betrayal is self-protection, not greed',
                'The Reluctant Femme Fatale: She genuinely loves the protagonist but is trapped by circumstances forcing her to betray him, creating genuine internal conflict',
                'The Amateur Femme Fatale: She attempts manipulation but lacks the skill or ruthlessness—her clumsy efforts reveal her fundamental humanity',
                'The Inverted Power Dynamic: The protagonist has been manipulating her while she believes she\'s in control—the gender power dynamic is completely reversed',
                'The Mutual Recognition: Both characters know the other is manipulating them and engage in the dance anyway, finding genuine connection within the deception'
            ]
        },
        3: {
            'title': 'The Dead Narrator Revelation',
            'convention': 'The shocking revelation that the protagonist has been narrating from beyond the grave, creating tragic irony and emphasizing fatalistic storytelling.',
            'subversions': [
                'The Dying Narrator: The protagonist is slowly dying throughout the story, and the narration becomes increasingly desperate and fragmented as death approaches',
                'The Metaphorically Dead Narrator: The narrator is "dead" inside—emotionally destroyed by events, speaking from a place of spiritual death rather than literal death',
                'The Future Dead Narrator: The narrator knows they will die and narrates with the weight of inevitable doom, creating dramatic irony about timing',
                'The Preserved Narrator: The narrator survived but lost everyone they cared about—they\'re narrating from a life that feels like death',
                'The Witness Protection Narrator: The narrator had to "die" officially and narrates from their new identity, unable to return to their old life'
            ]
        },
        4: {
            'title': 'The Corrupt Authority Figure Twist',
            'convention': 'The trusted law enforcement officer is revealed as thoroughly corrupt, representing institutional decay and the impossibility of justice through legitimate channels.',
            'subversions': [
                'The Reluctant Corruption: The authority figure became corrupt to protect their family or prevent greater evil—their corruption stems from desperation, not greed',
                'The Selective Corruption: They\'re corrupt regarding specific cases but genuinely honest about everything else, creating moral complexity',
                'The Inherited Corruption: They discovered the corruption was systematic and inherited, trapping them in a web they didn\'t create but cannot escape',
                'The Justified Corruption: Their corrupt acts actually serve justice better than following the law would—challenging the moral framework itself',
                'The Failed Redemption: They were corrupt but genuinely tried to reform, only to be pulled back by circumstances or threats to others'
            ]
        },
        5: {
            'title': 'The Switched Identity Discovery',
            'convention': 'Characters assume false identities to survive or escape their past, often taking dead men\'s papers and creating new lives built on deception.',
            'subversions': [
                'The Identity Theft Victim: The character discovers someone else has been living as them, forcing them to prove their own identity',
                'The Inherited Identity: The false identity comes with unexpected obligations, debts, and relationships the character must navigate',
                'The Identity Trap: The new identity was deliberately created as a trap, designed to ensnare whoever assumed it',
                'The Parallel Lives: The character discovers they\'re living a life nearly identical to their original one, questioning whether escape is possible',
                'The Identity Cascade: Assuming a false identity forces the character to adopt additional false identities to maintain the first deception'
            ]
        },
        6: {
            'title': 'The Amnesia Device',
            'convention': 'Memory loss drives both plot progression and psychological exploration, with characters forced to rediscover their own identity and past actions.',
            'subversions': [
                'The Selective Memory: The character remembers everything except the one crucial piece of information that would solve everything',
                'The False Memory: The character\'s "recovered" memories are actually implanted false memories designed to manipulate their actions',
                'The Protective Amnesia: The memory loss was self-induced to protect themselves or others from dangerous knowledge',
                'The Gradual Return: Memories return slowly and out of sequence, creating a distorted understanding of past events',
                'The Shared Amnesia: Multiple characters lost the same memories, suggesting external manipulation rather than accident or trauma'
            ]
        },
        7: {
            'title': 'The Partner\'s Betrayal',
            'convention': 'Trusted allies turn against protagonists at crucial moments, revealing hidden motivations and shattering bonds of loyalty when characters need support most.',
            'subversions': [
                'The Preemptive Betrayal: The partner betrays the protagonist to prevent the protagonist from betraying them first—a defensive move based on accurate assessment',
                'The Necessary Betrayal: The partner must betray the protagonist to save them from a worse fate they\'re walking toward unknowingly',
                'The Misunderstood Loyalty: What appears to be betrayal is actually the partner following the protagonist\'s secret instructions or earlier agreement',
                'The Institutional Betrayal: The partner remains personally loyal but is forced to betray by institutional pressures—duty versus friendship',
                'The Graduated Betrayal: The betrayal happens slowly over time as the partner\'s loyalties gradually shift, making the final moment feel inevitable rather than shocking'
            ]
        },
        8: {
            'title': 'First-Person Voice-Over Confession',
            'convention': 'Protagonists narrate their own downfall in confessional style, creating intimate yet doomed storytelling that emphasizes personal responsibility.',
            'subversions': [
                'The Defensive Confession: The narrator confesses to lesser crimes to hide their involvement in worse ones',
                'The Proxy Confession: The narrator confesses someone else\'s crimes because they feel responsible for enabling them',
                'The Incomplete Confession: The narrator stops short of admitting the worst truth, leaving crucial information unrevealed',
                'The Coerced Confession: The confession is being extracted under threat, making its reliability questionable',
                'The Posthumous Confession: The confession is discovered after the narrator\'s death, leaving questions about their final intentions'
            ]
        },
        9: {
            'title': 'Unreliable Narrator Technique',
            'convention': 'Multiple perspectives create confusion about actual events, with the narrator\'s bias, mental state, or deliberate deception distorting the truth.',
            'subversions': [
                'The Emotionally Unreliable Narrator: The narrator tells the truth about events but their emotional interpretation colors everything, making the same facts feel completely different',
                'The Professionally Unreliable Narrator: A trained investigator whose expertise makes them see patterns and connections that may not exist, leading to elaborate but false theories',
                'The Temporally Displaced Narrator: The narrator experienced events out of sequence due to trauma, memory loss, or other factors, creating confusion about causality',
                'The Inverse Reliability: The narrator lies about small, irrelevant details but tells the absolute truth about important events—forcing readers to distinguish significance',
                'The Competing Reliability: Multiple narrators each believe they\'re telling the truth, but their accounts contradict because they witnessed different aspects of complex events'
            ]
        },
        10: {
            'title': 'Framed Flashback Structure (A-B-A Pattern)',
            'convention': 'Present-day scenes bookend extended flashbacks, creating a sense of inevitability and doom as past events lead inexorably to the current situation.',
            'subversions': [
                'The Altered Present: The present-day frame changes based on the flashbacks, suggesting the act of remembering is changing current reality',
                'The Multiple Presents: Different flashbacks lead to different present-day scenarios, questioning which timeline is real',
                'The Incomplete Frame: The flashback extends beyond the present-day frame, revealing the current situation isn\'t the end of the story',
                'The False Present: The "present-day" frame is revealed to be another flashback from an even later time period',
                'The Causal Loop: The present-day events are caused by the character telling the flashback story, creating a temporal paradox'
            ]
        },
        11: {
            'title': 'Nested Flashbacks',
            'convention': 'Flashbacks within flashbacks create complex temporal structures that mirror the psychological complexity of memory and layered truth.',
            'subversions': [
                'The Contradictory Nest: Each nested flashback contradicts the one containing it, suggesting memory is actively rewriting itself',
                'The Deepening Perspective: Each nested level reveals information that recontextualizes all the outer levels',
                'The Escape Mechanism: Characters use nested flashbacks to avoid confronting present-day reality',
                'The Inherited Memory: Nested flashbacks contain other people\'s memories, suggesting psychological contamination or shared trauma',
                'The Temporal Bleeding: Events from different nested levels start affecting each other, blurring the boundaries between past and present'
            ]
        },
        12: {
            'title': 'Multiple Flashback Narrators',
            'convention': 'Different characters provide conflicting versions of events, using various perspectives to construct the narrative while highlighting subjective truth.',
            'subversions': [
                'The Partial Witnesses: Each narrator only witnessed part of the events, requiring their accounts to be combined to understand the full truth',
                'The Motivated Revisions: Each narrator alters their account to protect someone they care about, making all versions lies of omission',
                'The Degraded Transmission: Each narrator heard the story from someone else, creating a game of telephone that distorts the original events',
                'The Complementary Blindness: Each narrator has specific blind spots that the others compensate for, making individual accounts useless but collective accounts complete',
                'The Temporal Displacement: The narrators are recounting events from different time periods, making comparison impossible'
            ]
        },
        13: {
            'title': 'The Peeling Onion Structure',
            'convention': 'Each clue leads to new complications rather than solutions, with the mystery deepening and becoming more complex as more information is revealed.',
            'subversions': [
                'The False Complexity: The apparent complexity is a deliberate smokescreen hiding a simple truth that would be devastating if revealed',
                'The Recursive Mystery: Solving the mystery reveals it was created to distract from the real mystery, which was created to distract from an even deeper mystery',
                'The Simplifying Investigation: Each clue actually eliminates possibilities and narrows focus, but the truth becomes more terrible as options disappear',
                'The Parallel Mysteries: Multiple separate mysteries appear to be one complex mystery, leading investigators down wrong paths',
                'The Self-Generating Mystery: The investigation itself creates new mysteries by changing the behavior of people being investigated'
            ]
        },
        14: {
            'title': 'Multiple Interrogation Scenes',
            'convention': 'Investigators interview different characters whose stories form the narrative core, with each session revealing new information while casting doubt on previous revelations.',
            'subversions': [
                'The Reverse Interrogation: Each suspect learns more about the investigator than they reveal about themselves, gradually building a profile of their questioner',
                'The Contaminated Interrogation: Each interrogation is influenced by information from previous ones, making later accounts unreliable',
                'The Protective Lies: Each character lies to protect someone else, creating a web of false information motivated by loyalty rather than guilt',
                'The Escalating Truth: Each interrogation reveals more devastating truths, but also makes the consequences of those truths more severe',
                'The Incomplete Sessions: Each interrogation is interrupted or cut short, leaving crucial information unrevealed and building tension'
            ]
        },
        15: {
            'title': 'The Red Herring Pattern',
            'convention': 'False leads deliberately mislead both protagonist and audience, with apparent clues that point toward incorrect conclusions about the crime.',
            'subversions': [
                'The Accidental Red Herring: Genuine clues are misinterpreted due to the investigator\'s biases or assumptions, making real evidence misleading',
                'The Reverse Red Herring: Obviously false clues are planted to make investigators ignore them, but they actually contain hidden truth',
                'The Personal Red Herring: The false clues are created by the investigator\'s own psychological needs rather than deliberate misdirection',
                'The Temporal Red Herring: Clues from different time periods get mixed together, making past evidence appear to relate to current crimes',
                'The Emotional Red Herring: The investigator follows false leads because they want them to be true, rather than because the evidence supports them'
            ]
        },
        16: {
            'title': 'The Gradual Revelation Structure',
            'convention': 'Information is parceled out in controlled doses, with each revelation complicating rather than clarifying the situation.',
            'subversions': [
                'The Information Cascade: Each revelation triggers an avalanche of additional information that overwhelms the characters\' ability to process it',
                'The Delayed Comprehension: All information is available early, but its significance only becomes clear retrospectively',
                'The Misleading Sequence: The order in which information is revealed creates false impressions about causality and motivation',
                'The Competing Revelations: Multiple sources provide information simultaneously, forcing characters to choose which version to believe',
                'The Retroactive Revelation: New information changes the meaning of everything previously revealed, requiring constant reinterpretation'
            ]
        },
        17: {
            'title': 'The Fateful Meeting',
            'convention': 'The initial encounter between key characters sets everything in motion, with seemingly routine interactions proving to be the catalyst for all subsequent tragedy.',
            'subversions': [
                'The Avoided Meeting: Characters desperately try to avoid meeting each other because they know it will lead to tragedy, but fate forces the encounter',
                'The Delayed Recognition: The characters met long ago but don\'t recognize each other until much later, revealing their connection was always present',
                'The Engineered Meeting: What appears to be chance was actually carefully orchestrated by a third party for their own purposes',
                'The Repeated Meeting: The characters keep encountering each other in different contexts, suggesting their connection transcends coincidence',
                'The Proxy Meeting: The characters never actually meet, but their lives become intertwined through intermediaries and shared experiences'
            ]
        },
        18: {
            'title': 'The Point of No Return',
            'convention': 'Characters cross moral lines they cannot uncross, with specific moments marking the irreversible descent into criminality or doom.',
            'subversions': [
                'The Invisible Line: The character crosses the point of no return without realizing it, making the moral fall unconscious rather than deliberate',
                'The False Point: What appears to be the point of no return is revealed to be reversible, but the character\'s belief that it wasn\'t has changed them permanently',
                'The Incremental Descent: There is no single point of no return, just a gradual slide where each small compromise makes the next one easier',
                'The Necessary Evil: The character must cross the line to prevent something worse, making the moral fall a sacrifice rather than a corruption',
                'The Retroactive Point: The point of no return is identified only in retrospect, when escape was still possible but psychological commitment had already occurred'
            ]
        },
        19: {
            'title': 'The Dying Confession',
            'convention': 'Characters reveal crucial truth only when facing death, with final moments bringing honesty and the revelation of important secrets.',
            'subversions': [
                'The False Death Confession: The character believes they\'re dying but survives, leaving them to deal with the consequences of their revealed secrets',
                'The Incomplete Confession: Death interrupts the confession at the crucial moment, leaving the most important information unrevealed',
                'The Transferred Guilt: The dying character confesses to crimes they didn\'t commit to protect someone else, taking secrets to the grave',
                'The Rejected Confession: The dying character tries to confess but others refuse to listen, either from denial or to preserve their memory',
                'The Misunderstood Confession: The confession is delivered in metaphorical or coded language that is misinterpreted by those who hear it'
            ]
        },
        20: {
            'title': 'The False Rescue Attempt',
            'convention': 'Apparent salvation proves to be another trap, with rescue attempts that deepen the protagonist\'s entanglement rather than providing escape.',
            'subversions': [
                'The Genuine Rescue with Hidden Cost: The rescue is real but comes with unexpected obligations or consequences that prove worse than the original danger',
                'The Self-Rescue: The protagonist must rescue themselves when their supposed rescuer proves unreliable or has ulterior motives',
                'The Mutual Rescue: Both parties are trying to rescue each other from the same danger, creating confusion about who needs saving',
                'The Delayed Rescue: The rescue arrives too late to prevent the main damage but early enough to prevent recovery or healing',
                'The Unwanted Rescue: The protagonist doesn\'t want to be rescued because they\'ve found meaning or purpose in their dangerous situation'
            ]
        },
        21: {
            'title': 'The Femme Fatale\'s Multiple Betrayals',
            'convention': 'Women betray husbands, lovers, and associates in endless cycles, with each relationship revealing new layers of manipulation and deception.',
            'subversions': [
                'The Escalating Betrayals: Each betrayal is motivated by the consequences of the previous one, creating a cycle of defensive deception',
                'The Loyal Betrayer: She remains emotionally faithful to each person while betraying them professionally, separating personal and business relationships',
                'The Inherited Betrayals: Her betrayals are following a pattern established by someone else, making her a victim of circumstance rather than a calculating manipulator',
                'The Protective Betrayals: Each betrayal is designed to save the victim from something worse, making her actions altruistic rather than selfish',
                'The Involuntary Betrayals: External circumstances force her into betrayal against her will, making her a tragic figure rather than a villain'
            ]
        },
        22: {
            'title': 'The Client\'s Hidden Agenda',
            'convention': 'The person hiring the detective has ulterior motives beyond the stated case, with the real purpose being manipulation or deception of the investigator.',
            'subversions': [
                'The Evolving Agenda: The client\'s hidden agenda changes as the investigation progresses, forcing them to improvise deception',
                'The Protective Agenda: The hidden agenda is designed to protect the detective from knowledge that would harm them',
                'The Transferred Agenda: The client is pursuing someone else\'s hidden agenda without knowing it, making them a unwitting proxy',
                'The Competing Agendas: The client has multiple conflicting hidden agendas and must choose which to prioritize as the case develops',
                'The Exposed Agenda: The detective discovers the hidden agenda early but pretends not to know, creating a game of double deception'
            ]
        },
        23: {
            'title': 'The Authority Figure\'s Corruption',
            'convention': 'Police corruption forces honest cops to work outside the system, with institutional decay making official channels unreliable for justice.',
            'subversions': [
                'The Systemic Corruption: The corruption is so pervasive that honest behavior becomes the aberration, making good cops the problem',
                'The Historical Corruption: Current corruption is the result of past injustices that created cynicism and moral compromise',
                'The Defensive Corruption: Corruption developed as protection against external threats, making it a survival mechanism rather than greed',
                'The Compartmentalized Corruption: Different parts of the system have different types of corruption that sometimes conflict with each other',
                'The Reform Corruption: Attempts to eliminate corruption create new forms of corruption, making moral improvement impossible'
            ]
        },
        24: {
            'title': 'The Gang Member\'s Defection',
            'convention': 'Criminal organizations turn on their own members during and after crimes, with loyalty breaking down under pressure and self-interest.',
            'subversions': [
                'The Loyalty Test: The apparent defection is actually a test of other members\' loyalty, orchestrated by the organization itself',
                'The Forced Defection: External pressure forces the defection against the member\'s will, creating genuine conflict between duty and survival',
                'The Ideological Defection: The member defects because the organization has changed its principles, not because of self-interest',
                'The Sacrificial Defection: The member defects to draw attention away from the organization, sacrificing themselves for the group\'s survival',
                'The Inherited Defection: The defection continues a pattern established by previous generations, making it inevitable rather than chosen'
            ]
        },
        25: {
            'title': 'Valuable Objects',
            'convention': 'Precious items drive character motivations but often prove illusory or corrupting, with the pursuit of wealth revealing moral corruption.',
            'subversions': [
                'The Cursed Value: The object brings misfortune to anyone who possesses it, making its value a liability rather than an asset',
                'The Conditional Value: The object is only valuable under specific circumstances that may not continue to exist',
                'The Shared Value: The object must be possessed collectively to have any worth, forcing cooperation among competitors',
                'The Diminishing Value: The object loses value each time it changes hands, making immediate use more important than long-term possession',
                'The Transformative Value: Possessing the object changes the owner in ways that make its original value irrelevant'
            ]
        },
        26: {
            'title': 'Missing Persons',
            'convention': 'Disappeared individuals motivate investigations, with the search revealing deeper mysteries about identity, relationships, and hidden motivations.',
            'subversions': [
                'The Voluntary Disappearance: The missing person orchestrated their own disappearance to escape unbearable circumstances',
                'The Mistaken Identity: The "missing" person never existed, and the search reveals identity theft or deception',
                'The Parallel Disappearance: Multiple people disappeared for different reasons, but their cases become conflated during investigation',
                'The Protective Disappearance: The person disappeared to protect others from danger associated with their presence',
                'The Gradual Disappearance: The person disappeared slowly from their old life while building a new one, making the disappearance barely noticeable'
            ]
        },
        27: {
            'title': 'Compromising Photographs or Documents',
            'convention': 'Evidence becomes dangerous currency, with knowledge proving as valuable and deadly as money, creating blackmail opportunities and power struggles.',
            'subversions': [
                'The Context-Dependent Evidence: The compromising material only appears damaging when viewed without proper context',
                'The Planted Evidence: The compromising material was created specifically to be discovered, serving someone else\'s agenda',
                'The Obsolete Evidence: What was once compromising is no longer damaging due to changing social attitudes or circumstances',
                'The Shared Compromise: The evidence is compromising to multiple parties equally, creating mutual vulnerability rather than one-sided power',
                'The Self-Destroying Evidence: The act of using the evidence for blackmail destroys its effectiveness or credibility'
            ]
        },
        28: {
            'title': 'The Insurance Scam',
            'convention': 'Insurance fraud plots combine greed with elaborate planning, using the complexity of insurance systems to enable sophisticated criminal schemes.',
            'subversions': [
                'The Accidental Fraud: Characters unintentionally commit insurance fraud through misunderstanding or bad advice',
                'The Defensive Fraud: The fraud is committed to recover money already stolen by the insurance company through legitimate but unethical practices',
                'The Moral Fraud: Characters commit fraud against an insurance company to fund charitable activities or help others',
                'The Exposed Fraud: The insurance company knows about the fraud but allows it for their own purposes',
                'The Cascading Fraud: One small fraudulent claim necessitates larger and larger frauds to maintain the deception'
            ]
        },
        29: {
            'title': 'Doom-Laden Openings',
            'convention': 'Films begin with crime scenes or aftermath, establishing a fatalistic atmosphere that promises tragedy and moral corruption.',
            'subversions': [
                'The False Doom: The ominous opening is revealed to be less serious than it appeared, but the atmosphere of doom persists anyway',
                'The Delayed Doom: The opening shows the end result, but the doom takes much longer to arrive than expected, building tension through anticipation',
                'The Transferred Doom: The doom foreshadowed in the opening affects different characters than expected',
                'The Escaped Doom: Characters successfully avoid the fate suggested by the opening, but their efforts to escape create different problems',
                'The Chosen Doom: Characters deliberately walk toward the doom shown in the opening because they believe it\'s necessary or justified'
            ]
        },
        30: {
            'title': 'Circular/Cyclical Endings',
            'convention': 'Stories end where they began, with protagonists returning to starting positions but fundamentally changed by their experiences.',
            'subversions': [
                'The Broken Cycle: Characters almost return to the beginning but break the pattern at the last moment, choosing a different path',
                'The Inherited Cycle: The protagonist escapes the cycle, but someone else takes their place, suggesting the cycle transcends individuals',
                'The Expanding Cycle: Each return to the beginning includes more people or higher stakes, making the cycle grow rather than repeat',
                'The Voluntary Cycle: Characters choose to repeat the cycle because they found meaning or purpose in the experience',
                'The Incomplete Cycle: The story ends before reaching the beginning again, leaving the cycle unresolved and the pattern broken'
            ]
        },
        31: {
            'title': 'Pyrrhic Victory Endings',
            'convention': 'Justice is served but at great cost, with moral order restored through punishment and sacrifice that destroys most characters involved.',
            'subversions': [
                'The Delayed Cost: The victory appears complete initially, but the costs accumulate over time until the victory becomes pyrrhic retrospectively',
                'The Chosen Cost: Characters deliberately accept terrible costs because they believe the victory is worth any price',
                'The Transferred Cost: The victory\'s cost is paid by people who weren\'t involved in achieving it, raising questions about justice',
                'The Generational Cost: The cost of victory affects future generations rather than the current participants',
                'The Invisible Cost: The victory\'s true cost is hidden or delayed, making characters unaware of what they\'ve sacrificed'
            ]
        },
        32: {
            'title': 'The Last-Minute Reversal',
            'convention': 'Final scenes reveal new information that recontextualizes the entire story, with last-second revelations that change everything previously understood.',
            'subversions': [
                'The Anticipated Reversal: Characters expect a last-minute reversal and prepare for it, but the preparation creates the very reversal they feared',
                'The Partial Reversal: The revelation changes some but not all previous understanding, creating a mixed recontextualization',
                'The False Reversal: The apparent reversal is itself misleading, designed to distract from the real truth',
                'The Cascading Reversal: One reversal triggers a series of additional reversals that keep changing the story\'s meaning',
                'The Character-Driven Reversal: The reversal comes from character development rather than plot revelation, making it psychological rather than informational'
            ]
        },
        33: {
            'title': 'The Planted Evidence Technique',
            'convention': 'Corrupt officials manipulate crime scenes to frame innocents, using their authority to create false narratives that support their agenda.',
            'subversions': [
                'The Self-Incriminating Plant: The planted evidence accidentally implicates the person who planted it rather than the intended target',
                'The Historical Plant: Evidence planted long ago for a different purpose becomes relevant to current crimes by coincidence',
                'The Competing Plants: Multiple parties plant different evidence at the same scene, creating confusion rather than clear framing',
                'The Protective Plant: Evidence is planted to protect someone by making them appear guilty of a lesser crime to hide their involvement in a worse one',
                'The Obsolete Plant: Planted evidence becomes irrelevant due to changing circumstances, but its discovery still creates problems'
            ]
        },
        34: {
            'title': 'The Double Insurance Policy',
            'convention': 'Multiple parties insure the same person or object for different reasons, creating complex webs of motivation where everyone benefits from the same loss.',
            'subversions': [
                'The Conflicting Policies: Insurance policies have contradictory terms that make simultaneous collection impossible',
                'The Unknown Policies: Parties don\'t know about each other\'s policies, leading to unintended cooperation or conflict',
                'The Escalating Policies: Each new policy is taken out in response to previous ones, creating an arms race of insurance coverage',
                'The Protective Policies: Policies are taken out to protect against other policyholders rather than external threats',
                'The Inherited Policies: Insurance obligations are passed down through generations, creating long-term complications'
            ]
        },
        35: {
            'title': 'The Blackmail Chain',
            'convention': 'Characters blackmail each other in interconnected webs, with each revelation creating new vulnerabilities and opportunities for manipulation.',
            'subversions': [
                'The Emotional Blackmail Chain: Characters hold each other\'s deepest fears and insecurities rather than criminal secrets',
                'The Protective Blackmail: Each person in the chain is being blackmailed to protect someone they love',
                'The Information Cascade: Each revelation in the blackmail chain makes previous secrets irrelevant',
                'The Time-Sensitive Blackmail: The blackmail material becomes more or less damaging over time, creating urgency around timing',
                'The Mutual Blackmail: Everyone has equally damaging information about everyone else, creating stable deterrence'
            ]
        },
        36: {
            'title': 'The Witness Protection Failure',
            'convention': 'Characters hiding from their past find their new identities discovered and threatened, with the protective system proving inadequate against determined enemies.',
            'subversions': [
                'The Internal Leak: The protection fails because someone within the system betrays the witness for personal reasons',
                'The Inherited Danger: The witness\'s new identity has its own enemies and dangers unrelated to their original problems',
                'The Technological Failure: Modern technology makes anonymity impossible, regardless of official protection efforts',
                'The Voluntary Exposure: The witness deliberately reveals themselves because hiding has become more unbearable than facing their enemies',
                'The Mistaken Identity: The witness is threatened because they\'re confused with someone else who should be in protection'
            ]
        },
        37: {
            'title': 'The Criminal\'s Return',
            'convention': 'Deported or imprisoned criminals attempt comebacks, bringing old conflicts back to life and threatening the stability characters thought they had achieved.',
            'subversions': [
                'The Changed Criminal: The returning criminal has genuinely reformed but is treated as if they haven\'t, forcing them back into crime',
                'The Inherited Conflict: The criminal\'s return affects their children or associates rather than their original enemies',
                'The Mistimed Return: The criminal returns when their enemies are no longer in power, making their comeback irrelevant',
                'The Welcomed Return: The criminal\'s return is actually needed to solve current problems, making them a reluctant ally',
                'The Phantom Return: Fear of the criminal\'s return affects everyone\'s behavior even though they never actually come back'
            ]
        },
        38: {
            'title': 'The Mob Connection',
            'convention': 'Seemingly independent crimes trace back to organized criminal networks, revealing larger conspiracies behind apparently local or personal conflicts.',
            'subversions': [
                'The False Connection: Coincidental similarities make unrelated crimes appear connected to organized crime',
                'The Reluctant Connection: Criminals are forced into mob involvement against their will to protect family or friends',
                'The Historical Connection: The mob connection is from past generations, affecting current characters who don\'t know about it',
                'The Competing Mobs: Multiple criminal organizations claim the same territory or crimes, creating internal conflicts',
                'The Dissolved Connection: The criminal organization no longer exists, but its reputation and structure continue to influence behavior'
            ]
        },
        39: {
            'title': 'The Corrupt Business Partnership',
            'convention': 'Legitimate businesses serve as fronts for criminal operations, with respectable facades hiding illegal enterprises and criminal conspiracies.',
            'subversions': [
                'The Unknowing Partnership: One partner genuinely doesn\'t know about the criminal activities and becomes complicit accidentally',
                'The Forced Partnership: The business is coerced into serving as a front through threats or blackmail',
                'The Historical Partnership: The criminal connection is from the business\'s past, but current owners must deal with ongoing consequences',
                'The Competing Loyalties: Partners have conflicting criminal obligations that make cooperation impossible',
                'The Inherited Partnership: Criminal obligations are passed down with business ownership, trapping new owners'
            ]
        },
        40: {
            'title': 'The Frame-Up Investigation',
            'convention': 'Protagonists must prove their innocence while being pursued by both criminals and law enforcement, creating pressure from multiple directions with nowhere safe to turn.',
            'subversions': [
                'The Accidental Frame: The protagonist was framed unintentionally as collateral damage in a different scheme',
                'The Self-Fulfilling Frame: The process of being framed actually makes the protagonist commit the crimes they were falsely accused of',
                'The Protective Frame: Someone who cares about the protagonist framed them to keep them away from greater danger',
                'The Historical Frame: The protagonist is framed for crimes that mirror historical injustices, adding layers of social commentary',
                'The Recursive Frame: Investigating the frame-up reveals the protagonist actually did commit different crimes, making their innocence complicated'
            ]
        }
    }
    
    # Generate the requested number of tropes
    result = []
    trope_numbers = list(tropes_data.keys())
    
    for _ in range(num_tropes):
        # Randomly select a trope
        trope_num = random.choice(trope_numbers)
        trope_data = tropes_data[trope_num]
        trope_title = trope_data['title']
        
        # Decide whether to use convention or subversion
        if random.random() < subversion_percentage:
            # Use a random subversion
            subversion = random.choice(trope_data['subversions'])
            implementation_type = "Subversion"
            implementation = subversion
        else:
            # Use the convention
            implementation_type = "Convention"
            implementation = trope_data['convention']
        
        result.append((trope_title, implementation_type, implementation))
    
    return result

# Demonstration of the function
if __name__ == "__main__":
    print("=== REVISED NOIR TROPE GENERATOR ===\n")
    
    # Generate a list with 30% subversion rate
    print("Generated Noir Story Elements (30% subversion rate):")
    print("=" * 60)
    
    tropes = generate_noir_tropes(subversion_percentage=0.3, num_tropes=15)
    
    for i, (title, impl_type, description) in enumerate(tropes, 1):
        print(f"{i}. {title}")
        print(f"   Type: {impl_type}")
        print(f"   Implementation: {description}")
        print()
    
    print("\n" + "=" * 60)
    print(f"Summary: {len([t for t in tropes if t[1] == 'Convention'])} conventional implementations, "
          f"{len([t for t in tropes if t[1] == 'Subversion'])} subversions")
    
    # Example with higher subversion rate
    print("\n\nHigh Subversion Example (70% subversion rate):")
    print("=" * 50)
    
    high_subversion_tropes = generate_noir_tropes(subversion_percentage=0.7, num_tropes=8)
    
    for i, (title, impl_type, description) in enumerate(high_subversion_tropes, 1):
        marker = "🔄" if impl_type == "Subversion" else "📖"
        print(f"{marker} {title}: {description[:100]}...")
    
    print(f"\nSubversion rate: {len([t for t in high_subversion_tropes if t[1] == 'Subversion'])} / {len(high_subversion_tropes)}")

# Example usage:
# conventional_story = generate_noir_tropes(subversion_percentage=0.0, num_tropes=10)
# subversive_story = generate_noir_tropes(subversion_percentage=1.0, num_tropes=10)
# mixed_story = generate_noir_tropes(subversion_percentage=0.4, num_tropes=20)