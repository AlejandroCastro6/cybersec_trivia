#!/usr/bin/env python3
"""
CyberQuest: Who Wants to Be a Cyber Expert?
WWTBAM-style exam prep for CSI6199 - Masters in Cyber Security.
"""

import time
import random
import os
import sys

# ── ANSI colours ──────────────────────────────────────────────────────────────
R = "\033[0m"
BOLD = "\033[1m"
DIM = "\033[2m"
RED = "\033[91m"
GRN = "\033[92m"
YLW = "\033[93m"
BLU = "\033[94m"
MGT = "\033[95m"
CYN = "\033[96m"
WHT = "\033[97m"
BG_BLU = "\033[44m"
BG_GRN = "\033[42m"
BG_RED = "\033[41m"
BG_YLW = "\033[43m"
BG_MGT = "\033[45m"

# ── Prize ladder ──────────────────────────────────────────────────────────────
PRIZES = [
    "$100", "$200", "$300", "$500", "$1,000",
    "$2,000", "$4,000", "$8,000", "$16,000", "$32,000",
    "$64,000", "$125,000",
]
SAFE_HAVENS = {4, 9}   # 0-based indices; questions 5 and 10

# ── Questions bank ────────────────────────────────────────────────────────────
# Format per question:
#   "q"    : question text
#   "opts" : {"A": ..., "B": ..., "C": ..., "D": ...}
#   "ans"  : correct letter
#   "hint" : one-sentence hint (lifeline)
#   "diff" : 1=easy, 2=medium, 3=hard

MODULES = {
    "Module 1 – Intro to Cyber Security": [
        {
            "q": "The CIA triad in cyber security stands for three core aims. Which option correctly identifies all three?",
            "opts": {"A": "Confidentiality, Integrity, Availability",
                     "B": "Control, Integrity, Authentication",
                     "C": "Confidentiality, Identity, Availability",
                     "D": "Compliance, Integrity, Accountability"},
            "ans": "A", "diff": 1,
            "hint": "It's the most famous acronym in security — think of protecting data in all states.",
        },
        {
            "q": "Which cyber security aim ensures that information can only be read by authorised people?",
            "opts": {"A": "Availability", "B": "Integrity",
                     "C": "Confidentiality", "D": "Non-repudiation"},
            "ans": "C", "diff": 1,
            "hint": "The 'C' in CIA — keeping secrets secret.",
        },
        {
            "q": "What is a 'vulnerability' in the context of cyber security?",
            "opts": {
                "A": "A deliberate attack on a system",
                "B": "A flaw or weakness in the design, implementation or operation of a system",
                "C": "A piece of malware that exploits a network",
                "D": "An event that causes financial harm to an organisation"},
            "ans": "B", "diff": 1,
            "hint": "Think of it as the unlocked window that a threat can exploit.",
        },
        {
            "q": "Social engineering works primarily by exploiting which element?",
            "opts": {"A": "Firewall rules", "B": "Operating system flaws",
                     "C": "Human weaknesses and psychology", "D": "Network protocols"},
            "ans": "C", "diff": 1,
            "hint": "Kevin Mitnick said most people aren't trained to recognise this type of attack.",
        },
        {
            "q": "Which social engineering technique uses fraudulent *bulk* emails to steal sensitive information?",
            "opts": {"A": "Spear phishing", "B": "Pharming",
                     "C": "Vishing", "D": "Phishing"},
            "ans": "D", "diff": 2,
            "hint": "It's a fishing metaphor — cast a wide net and hope someone bites.",
        },
        {
            "q": "Which risk control strategy involves removing an asset entirely from the environment to eliminate a risk?",
            "opts": {"A": "Mitigate", "B": "Transfer",
                     "C": "Terminate", "D": "Accept"},
            "ans": "C", "diff": 2,
            "hint": "Sometimes the safest option is simply to stop doing the risky thing altogether.",
        },
        {
            "q": "According to Cialdini's 6 principles of influence, which principle involves giving a target a gift expecting them to share confidential information in return?",
            "opts": {"A": "Authority", "B": "Scarcity",
                     "C": "Reciprocity", "D": "Social Proof"},
            "ans": "C", "diff": 2,
            "hint": "You scratch my back, I'll scratch yours — attackers exploit this social norm.",
        },
        {
            "q": "Which aim of cyber security ensures that an entity CANNOT falsely deny performing an action?",
            "opts": {"A": "Availability", "B": "Authenticity",
                     "C": "Non-repudiation", "D": "Integrity"},
            "ans": "C", "diff": 2,
            "hint": "Alice sent an email — can she later deny it? This aim says no.",
        },
        {
            "q": "Which social engineering technique uses VoIP calls pretending to be from legitimate organisations to extract information?",
            "opts": {"A": "Pharming", "B": "Vishing",
                     "C": "Spear phishing", "D": "Reverse social engineering"},
            "ans": "B", "diff": 3,
            "hint": "Voice + phishing = this technique. The 'V' is the clue.",
        },
        {
            "q": "What is 'pharming'?",
            "opts": {
                "A": "Mass mailing of malicious attachments",
                "B": "Impersonating someone on the phone",
                "C": "Redirecting a target to a compromised website using phishing techniques",
                "D": "Installing keyloggers via USB drives"},
            "ans": "C", "diff": 3,
            "hint": "It hijacks your destination — you think you're going to your bank, but you land somewhere else.",
        },
        {
            "q": "According to the module, why is it psychologically difficult to 'sell' security to consumers?",
            "opts": {
                "A": "Security products are always too expensive",
                "B": "People prefer buying something they can see and use rather than a defence against something they want to avoid",
                "C": "Consumers distrust technology companies",
                "D": "Security software causes too many system slowdowns"},
            "ans": "B", "diff": 3,
            "hint": "Bruce Schneier's quote captures the core psychological resistance perfectly.",
        },
        {
            "q": "The concept of 'Defence in Depth' suggests that security should be:",
            "opts": {
                "A": "Applied only at the network perimeter",
                "B": "Layered across multiple levels so that a single failure does not compromise everything",
                "C": "Focused entirely on user education and training",
                "D": "Based on a single comprehensive firewall solution"},
            "ans": "B", "diff": 3,
            "hint": "Think of a castle — walls, moat, archers, and guards inside too.",
        },
    ],

    "Module 2 – Linux & Cyber Security": [
        {
            "q": "In Linux, which user is equivalent to the Windows 'administrator' and has the highest privileges?",
            "opts": {"A": "sudo", "B": "kali", "C": "root", "D": "admin"},
            "ans": "C", "diff": 1,
            "hint": "It's the super-user — the boss of all bosses in a Linux system.",
        },
        {
            "q": "Which command changes the ownership of a file in Linux?",
            "opts": {"A": "chmod", "B": "chown", "C": "chgrp", "D": "sudo"},
            "ans": "B", "diff": 1,
            "hint": "'ch' means change and 'own' means ownership — put them together.",
        },
        {
            "q": "What does the Linux 'pwd' command display?",
            "opts": {
                "A": "Prints the password policy for the current user",
                "B": "Lists processes with wide detail",
                "C": "Prints the absolute path of the current working directory",
                "D": "Shows the current user's password hash"},
            "ans": "C", "diff": 1,
            "hint": "Print Working Directory — tells you exactly where you are in the file system.",
        },
        {
            "q": "In a Linux path, what does '../' represent?",
            "opts": {
                "A": "The root directory",
                "B": "The current directory",
                "C": "One directory level up (parent directory)",
                "D": "A hidden file"},
            "ans": "C", "diff": 1,
            "hint": "Two dots means go back up a level — useful in relative paths.",
        },
        {
            "q": "In Linux file permissions 'rw-r-----', what can members of the file's GROUP do?",
            "opts": {
                "A": "Read, write and execute",
                "B": "Read and write only",
                "C": "Read only",
                "D": "No permissions"},
            "ans": "C", "diff": 2,
            "hint": "The second set of three characters (r--) covers the group.",
        },
        {
            "q": "Which Linux command changes the permissions (mode) of a file?",
            "opts": {"A": "chown", "B": "ls -l", "C": "chmod", "D": "sudo"},
            "ans": "C", "diff": 2,
            "hint": "'ch' = change, 'mod' = mode — it controls read/write/execute bits.",
        },
        {
            "q": "Which Linux distribution is specifically designed for penetration testing and cyber security?",
            "opts": {"A": "Ubuntu", "B": "Debian", "C": "Fedora", "D": "Kali Linux"},
            "ans": "D", "diff": 2,
            "hint": "Named after the Hindu goddess of power — it comes pre-loaded with security tools.",
        },
        {
            "q": "When running 'ls -l' in Linux, what do the very first characters of each line (e.g., drwxr-xr-x) indicate?",
            "opts": {
                "A": "The size of the file",
                "B": "The file type and permission bits",
                "C": "The last modification date",
                "D": "The number of hard links"},
            "ans": "B", "diff": 2,
            "hint": "'d' means directory, '-' means file, followed by rwx for owner, group, others.",
        },
        {
            "q": "Why do many cyber security tools exist *only* as CLI (Command Line Interface) tools?",
            "opts": {
                "A": "GUIs are too insecure for security tools",
                "B": "CLI tools can be more easily scripted, automated and provide lower-level access",
                "C": "CLI tools require less disk space",
                "D": "Most security professionals cannot use graphical interfaces"},
            "ans": "B", "diff": 3,
            "hint": "Think about automation, scripting pipelines, and remote access via SSH.",
        },
        {
            "q": "In Linux, why must you use './' before running an executable in the current directory (e.g., ./script.sh)?",
            "opts": {
                "A": "It grants root privileges to the script",
                "B": "For security reasons, the current directory is not included in $PATH by default",
                "C": "It tells the system to use the bash interpreter",
                "D": "It makes the script readable by all users"},
            "ans": "B", "diff": 3,
            "hint": "The $PATH variable tells Linux where to look for commands — and '.' isn't in there by default.",
        },
        {
            "q": "What does the 'which' command tell you in Linux?",
            "opts": {
                "A": "Which user is currently logged in",
                "B": "The exact file path of the program that would be executed when you type a command",
                "C": "Which packages are installed",
                "D": "Which groups the current user belongs to"},
            "ans": "B", "diff": 3,
            "hint": "Try 'which python3' — it tells you the full path of the binary that will run.",
        },
        {
            "q": "Why is analysing Windows malware on a Linux machine considered safer?",
            "opts": {
                "A": "Linux firewalls are more advanced than Windows firewalls",
                "B": "Windows malware is typically designed to run on Windows and is unlikely to infect a Linux host",
                "C": "Linux automatically quarantines all incoming files",
                "D": "Linux has built-in antivirus software"},
            "ans": "B", "diff": 3,
            "hint": "Most Windows malware executables (.exe, .dll) simply cannot run natively on Linux.",
        },
    ],

    "Module 3 – Risk Management": [
        {
            "q": "What is the definition of 'risk' in cyber security?",
            "opts": {
                "A": "A known attack that has already occurred",
                "B": "The probability of suffering harm or loss through an event exploiting a vulnerability in an asset",
                "C": "Any software that has not been patched",
                "D": "A documented list of organisational weaknesses"},
            "ans": "B", "diff": 1,
            "hint": "Risk sits at the intersection of threat, vulnerability, asset and impact.",
        },
        {
            "q": "In risk management, what does the strategy 'Transfer' mean?",
            "opts": {
                "A": "Remove the asset from the environment",
                "B": "Apply a safeguard to reduce the risk",
                "C": "Shift the risk to other assets, processes or organisations",
                "D": "Accept that the risk might be realised"},
            "ans": "C", "diff": 1,
            "hint": "Think of insurance — you pay someone else to carry the financial burden of a risk.",
        },
        {
            "q": "What is the difference between a 'threat' and a 'vulnerability'?",
            "opts": {
                "A": "A threat is an attack; a vulnerability is the damage caused",
                "B": "A threat is something that could cause harm; a vulnerability is a weakness that could be exploited",
                "C": "They are synonyms in cyber security",
                "D": "A vulnerability is the attacker; a threat is the system weakness"},
            "ans": "B", "diff": 1,
            "hint": "The storm (threat) can enter through the broken window (vulnerability).",
        },
        {
            "q": "What is an 'asset' in the context of a risk assessment?",
            "opts": {
                "A": "A known attacker targeting the organisation",
                "B": "Any software vulnerability in a system",
                "C": "Something of value to an organisation — physical items, information, staff, etc.",
                "D": "A control put in place to reduce risk"},
            "ans": "C", "diff": 1,
            "hint": "What do you stand to lose? That's your asset — it has value worth protecting.",
        },
        {
            "q": "When using the risk control strategy 'Mitigate', what is the goal?",
            "opts": {
                "A": "Eliminate the threat entirely",
                "B": "Reduce the impact or likelihood of a threat being realised",
                "C": "Hand the risk over to an insurance company",
                "D": "Remove the vulnerable asset from the network"},
            "ans": "B", "diff": 2,
            "hint": "Example: backups won't stop ransomware, but they reduce the damage if it hits.",
        },
        {
            "q": "According to Schneier (2008), which statement about human risk perception is TRUE?",
            "opts": {
                "A": "People accurately assess risks they are familiar with",
                "B": "People tend to underestimate common risks and overestimate spectacular but rare ones",
                "C": "People are better at assessing anonymous risks than personified ones",
                "D": "People generally overestimate risks they choose to take voluntarily"},
            "ans": "B", "diff": 2,
            "hint": "More people die in car accidents than plane crashes — yet people fear flying more.",
        },
        {
            "q": "What is the main goal of a 'risk assessment' vs. 'risk management'?",
            "opts": {
                "A": "Risk assessment is broader — it includes purchasing controls; risk management is just analysis",
                "B": "Risk assessment is a formal method for identifying and analysing threats; risk management is the broader decision-making process",
                "C": "They are identical processes with different names",
                "D": "Risk management is for governments only; risk assessment is for businesses"},
            "ans": "B", "diff": 2,
            "hint": "Assessment is the analysis phase; management is the full lifecycle including planning and response.",
        },
        {
            "q": "Why should organisations use established risk frameworks and standards rather than inventing their own?",
            "opts": {
                "A": "Custom frameworks are illegal in Australia",
                "B": "Established standards are already understood, accepted and validated — no need to reinvent the wheel",
                "C": "Using a standard guarantees zero security incidents",
                "D": "Only government-endorsed standards are legally binding"},
            "ans": "B", "diff": 2,
            "hint": "ISO 31000 and similar frameworks save time and bring credibility to the process.",
        },
        {
            "q": "What is the key distinction between 'risk controls' and 'security controls'?",
            "opts": {
                "A": "Risk controls are illegal; security controls are mandatory",
                "B": "Risk controls are higher-level strategic decisions; security controls are granular technical techniques",
                "C": "Security controls deal with physical threats only; risk controls deal with digital threats",
                "D": "There is no distinction — they are the same thing"},
            "ans": "B", "diff": 3,
            "hint": "Decide to 'mitigate ransomware' (risk control) → implement automated offline backups (security control).",
        },
        {
            "q": "Why is it NOT feasible to control ALL risks in an organisation?",
            "opts": {
                "A": "Some risks are mathematically impossible to model",
                "B": "Controlling every risk can be prohibitively expensive, impractical and may prevent normal business operations",
                "C": "Government regulations prohibit spending beyond a fixed security budget",
                "D": "Modern attackers can always bypass any control"},
            "ans": "B", "diff": 3,
            "hint": "Security must balance protection with usability and cost — extremes in either direction fail.",
        },
        {
            "q": "In risk terminology, what does 'qualify' a risk mean versus 'quantify' a risk?",
            "opts": {
                "A": "Qualifying means eliminating; quantifying means documenting",
                "B": "Qualifying describes the properties and characteristics; quantifying determines a numerical value or scale",
                "C": "They are synonyms — both mean assigning a number to the risk",
                "D": "Qualifying is done by management; quantifying is done by engineers"},
            "ans": "B", "diff": 3,
            "hint": "Describe it (qualify) before you try to measure it (quantify).",
        },
        {
            "q": "After implementing a risk control strategy, what critical fact does the module highlight?",
            "opts": {
                "A": "The organisation is now fully protected and needs no further action",
                "B": "New controls alter the organisation's risk exposure, meaning different risks may now be more likely — the cycle must repeat",
                "C": "All remaining risks can safely be accepted",
                "D": "Controls must be reported to ACSC within 30 days"},
            "ans": "B", "diff": 3,
            "hint": "Adding a control changes the landscape — new threats emerge and old impacts shift.",
        },
    ],

    "Module 4 – Cryptography I": [
        {
            "q": "What is a 'cipher' in cryptography?",
            "opts": {
                "A": "A secret key stored on a server",
                "B": "The encrypted output of a message",
                "C": "An algorithm used to encrypt or decrypt data",
                "D": "A digital certificate used for identity verification"},
            "ans": "C", "diff": 1,
            "hint": "It's the recipe — the algorithm — not the ingredient or the dish.",
        },
        {
            "q": "What is the key difference between symmetric and asymmetric encryption?",
            "opts": {
                "A": "Symmetric is weaker; asymmetric always uses longer keys",
                "B": "Symmetric uses the same key for encryption and decryption; asymmetric uses a key pair (public/private)",
                "C": "Symmetric can only encrypt text; asymmetric can encrypt any data",
                "D": "Asymmetric is used only for storage; symmetric is used only for transmission"},
            "ans": "B", "diff": 1,
            "hint": "Think of a padlock: one key for both locking and unlocking (symmetric) vs. a letterbox (asymmetric).",
        },
        {
            "q": "In a Caesar cipher with a shift of 3, what would the letter 'A' become?",
            "opts": {"A": "C", "B": "D", "C": "B", "D": "E"},
            "ans": "B", "diff": 1,
            "hint": "A → B → C → D. Shifting three positions forward in the alphabet.",
        },
        {
            "q": "What is steganography?",
            "opts": {
                "A": "The study of breaking encryption",
                "B": "A process of concealing secret information within another digital object without drawing attention",
                "C": "An asymmetric encryption algorithm",
                "D": "A method of hashing passwords securely"},
            "ans": "B", "diff": 1,
            "hint": "It's hiding in plain sight — the message is there, you just don't know to look.",
        },
        {
            "q": "What is the core problem with symmetric key distribution?",
            "opts": {
                "A": "Symmetric keys are too short to be secure",
                "B": "Symmetric keys cannot encrypt large files",
                "C": "Securely sharing the secret key with all intended parties — if it's intercepted, all security is lost",
                "D": "Symmetric encryption is too slow for practical use"},
            "ans": "C", "diff": 2,
            "hint": "How do Alice and Bob agree on a secret key over an insecure channel? That's the problem.",
        },
        {
            "q": "What replaced DES as the US government standard for symmetric encryption in 2001?",
            "opts": {"A": "3DES", "B": "RSA", "C": "AES", "D": "SHA-256"},
            "ans": "C", "diff": 2,
            "hint": "NIST ran a competition and this won — it's what your encrypted zip files use today.",
        },
        {
            "q": "What is a 'brute force attack' in the context of cryptography?",
            "opts": {
                "A": "An attack that physically destroys hardware to extract keys",
                "B": "Systematically testing every possible key until the correct one is found",
                "C": "A social engineering attack targeting system administrators",
                "D": "An attack that uses SQL injection to bypass authentication"},
            "ans": "B", "diff": 2,
            "hint": "It's the exhaustive search — try all possibilities until one works. Guaranteed to succeed given enough time.",
        },
        {
            "q": "In block cipher modes of operation, what two core principles underpin block ciphers?",
            "opts": {
                "A": "Compression and redundancy",
                "B": "Confusion (substitution) and Diffusion (transposition)",
                "C": "Padding and chaining",
                "D": "Hashing and salting"},
            "ans": "B", "diff": 2,
            "hint": "Confusion hides the relationship between plaintext and ciphertext; diffusion spreads influence across the output.",
        },
        {
            "q": "A 10-character password using upper, lower, digits and special characters has an entropy equivalent to roughly how many bits?",
            "opts": {"A": "128 bits", "B": "256 bits", "C": "66 bits", "D": "10 bits"},
            "ans": "C", "diff": 3,
            "hint": "log2(94^10) ≈ 66 — much weaker than the 256-bit AES key it might unlock.",
        },
        {
            "q": "What is the One Time Pad (OTP) and what makes it theoretically unbreakable?",
            "opts": {
                "A": "A hardware token that generates 6-digit codes; unbreakable because codes expire in 30 seconds",
                "B": "A stream cipher where the key is truly random, as long as the message, used only once, and both copies destroyed after — mathematically unbreakable",
                "C": "A block cipher with a 512-bit key; unbreakable due to keyspace size",
                "D": "An asymmetric algorithm based on factoring large primes"},
            "ans": "B", "diff": 3,
            "hint": "Shannon proved it — but the impracticality of key distribution is its fatal flaw.",
        },
        {
            "q": "Why is breaking RSA computationally difficult?",
            "opts": {
                "A": "RSA keys change every second, making brute force impossible",
                "B": "RSA relies on the difficulty of factoring the product of two very large prime numbers",
                "C": "RSA uses the same key for all operations, making interception useless",
                "D": "RSA outputs are padded to random lengths, hiding the ciphertext length"},
            "ans": "B", "diff": 3,
            "hint": "Multiplying two primes is easy; finding those primes from the product is hard — that asymmetry is the security.",
        },
        {
            "q": "What is Elliptic Curve Cryptography (ECC) particularly suited for compared to RSA?",
            "opts": {
                "A": "ECC is better for encrypting very large files",
                "B": "ECC achieves equivalent security with much shorter keys, making it ideal for constrained devices like smart cards",
                "C": "ECC is only used for hashing, not encryption",
                "D": "ECC is the only algorithm approved by NIST"},
            "ans": "B", "diff": 3,
            "hint": "A 256-bit ECC key ≈ a 3072-bit RSA key — much less computational work.",
        },
    ],

    "Module 5 – Cryptography II": [
        {
            "q": "What is a 'hash function' in cryptography?",
            "opts": {
                "A": "A symmetric cipher that encrypts large blocks of data",
                "B": "A one-way function that converts any input into a fixed-length output (digest)",
                "C": "A method for digitally signing emails",
                "D": "A key exchange protocol used in TLS"},
            "ans": "B", "diff": 1,
            "hint": "You can hash any file to get a fingerprint — but you cannot reverse it to get the file back.",
        },
        {
            "q": "What is the 'avalanche effect' in cryptographic hash functions?",
            "opts": {
                "A": "A vulnerability where multiple inputs produce the same hash",
                "B": "Changing even one bit of the input causes a completely unpredictable change to the entire output",
                "C": "The slowing down of hash computations over time",
                "D": "An attack that gradually weakens a hash by feeding it similar inputs"},
            "ans": "B", "diff": 1,
            "hint": "Change 'hello' to 'Hello' — the SHA-256 output is completely different.",
        },
        {
            "q": "What is a digital certificate and what standard defines its format?",
            "opts": {
                "A": "An encrypted file; defined by PGP standard",
                "B": "A data structure binding an identity to a public key; defined by X.509 v3",
                "C": "A hardware token containing private keys; defined by FIPS 140-2",
                "D": "A password hash file; defined by RFC 2898"},
            "ans": "B", "diff": 1,
            "hint": "Your browser checks these every time you visit https:// — they prove the server is who it claims.",
        },
        {
            "q": "What is a Certificate Authority (CA)?",
            "opts": {
                "A": "A government body that regulates encryption exports",
                "B": "A trusted third party that signs and vouches for the validity of digital certificates",
                "C": "A database of all public keys on the Internet",
                "D": "The private key holder who signs their own certificate"},
            "ans": "B", "diff": 1,
            "hint": "DigiCert, Let's Encrypt — they're the trusted notaries of the internet.",
        },
        {
            "q": "What is a 'salt' in password storage, and why is it useful?",
            "opts": {
                "A": "An additional password the user must enter; prevents guessing",
                "B": "A random value added to the password before hashing, making rainbow table attacks infeasible",
                "C": "A secret key stored alongside the password hash to re-encrypt it",
                "D": "A biometric factor stored with the user's account"},
            "ans": "B", "diff": 2,
            "hint": "Same password + different salt = completely different hash. Rainbow tables become useless.",
        },
        {
            "q": "Why does hashing a password NOT increase its security if the password is weak?",
            "opts": {
                "A": "Hash functions are reversible for short passwords",
                "B": "Hashing does not add entropy — a predictable password hashes to a predictable, searchable value",
                "C": "Weak passwords use MD5 which is already broken",
                "D": "Most hash functions truncate short passwords"},
            "ans": "B", "diff": 2,
            "hint": "SHA-256('123456789') is well-known — you can literally Google it.",
        },
        {
            "q": "What is a HMAC (Hashed Message Authentication Code) used for?",
            "opts": {
                "A": "Encrypting messages with a shared symmetric key",
                "B": "Verifying both the integrity of a message AND that the sender knows a shared secret key",
                "C": "Generating public/private key pairs",
                "D": "Compressing large files before transmission"},
            "ans": "B", "diff": 2,
            "hint": "A plain MAC can be forged by a MitM attacker — HMAC prevents this with a secret key.",
        },
        {
            "q": "What is the 'hierarchy of trust' in Public Key Infrastructure (PKI)?",
            "opts": {
                "A": "A ranking of encryption algorithms by strength",
                "B": "A chain of digital signatures where CAs vouch for each other up to a root CA hard-coded in your software",
                "C": "A list of trusted users allowed to sign documents",
                "D": "The order in which certificates are checked for expiry"},
            "ans": "B", "diff": 2,
            "hint": "Your browser trusts a root CA → which trusts an intermediate CA → which signed the website's cert.",
        },
        {
            "q": "What is the difference between a Domain Validated (DV) and an Extended Validation (EV) certificate?",
            "opts": {
                "A": "DV certificates are stronger; EV is used only for email",
                "B": "DV only proves control over a domain; EV requires additional identity vetting of the organisation by the CA",
                "C": "They use different encryption algorithms — DV uses RSA, EV uses ECC",
                "D": "EV certificates expire faster than DV certificates"},
            "ans": "B", "diff": 3,
            "hint": "EV used to trigger the green address bar in browsers — it means extra identity checks were done.",
        },
        {
            "q": "MD5 is considered cryptographically broken. What specific property has it lost?",
            "opts": {
                "A": "Determinism — it produces different outputs for the same input",
                "B": "Collision resistance — it is easy to find two different inputs that produce the same MD5 hash",
                "C": "Pre-image resistance — given a hash, the original input can be recovered trivially",
                "D": "Speed — MD5 is too slow for modern systems"},
            "ans": "B", "diff": 3,
            "hint": "Practical collision attacks on MD5 have been known since the early 2000s.",
        },
        {
            "q": "What is 'Trust on First Use' (TOFU) and what is its main weakness?",
            "opts": {
                "A": "Trusting a certificate permanently after it has been signed by a CA; weakness is CA compromise",
                "B": "Accepting an unknown server's key on first connection and trusting it thereafter; weakness is that the first connection could be a MitM attack",
                "C": "A policy of trusting all users until they violate security; weakness is insider threats",
                "D": "Automatically generating certificates for internal services; weakness is key rotation complexity"},
            "ans": "B", "diff": 3,
            "hint": "SSH uses TOFU — the first connection requires you to verify the host key fingerprint out of band.",
        },
        {
            "q": "What is the 'Web of Trust' model used by PGP, and how does it differ from CA-based PKI?",
            "opts": {
                "A": "PGP uses a single global root CA; CA-based PKI uses many distributed CAs",
                "B": "PGP allows peers to sign each other's keys creating an interconnected community of trust; CA-based PKI uses a centralised hierarchy",
                "C": "PGP uses symmetric encryption for certificates; CA-based PKI uses asymmetric",
                "D": "PGP is used only for email; CA-based PKI is only for HTTPS"},
            "ans": "B", "diff": 3,
            "hint": "No central authority — your friend signs your key, and their friend trusts your friend, so...",
        },
    ],

    "Module 6 – Authentication I": [
        {
            "q": "What are the three commonly cited authentication factors?",
            "opts": {
                "A": "Something you know, something you have, something you are",
                "B": "Password, PIN, biometric",
                "C": "Username, password, security question",
                "D": "Token, certificate, password"},
            "ans": "A", "diff": 1,
            "hint": "Know (password), Have (card/token), Are (fingerprint) — the holy trinity of auth factors.",
        },
        {
            "q": "What is the difference between authentication and authorisation?",
            "opts": {
                "A": "They are synonyms — both verify identity",
                "B": "Authentication verifies who you are; authorisation determines what you are allowed to do",
                "C": "Authentication is for systems; authorisation is for users",
                "D": "Authorisation happens before authentication"},
            "ans": "B", "diff": 1,
            "hint": "'I know who you are' (auth) vs. 'here's what you're allowed to do' (authz).",
        },
        {
            "q": "What are 'rainbow tables' and what attack do they facilitate?",
            "opts": {
                "A": "Colour-coded access control lists for file permissions",
                "B": "Precomputed tables of password hashes used to rapidly look up the original password from a stolen hash",
                "C": "A database of known malware signatures",
                "D": "A list of common SQL injection payloads"},
            "ans": "B", "diff": 1,
            "hint": "Steal a hashed password file, look up the hash in the table — instant plaintext password.",
        },
        {
            "q": "What is 'identity enrolment'?",
            "opts": {
                "A": "The process of logging in to a system for the first time",
                "B": "The process of establishing an identity and registering it with a system, linking an entity to an identifier",
                "C": "Resetting a lost password through a help desk",
                "D": "Installing multi-factor authentication on a user account"},
            "ans": "B", "diff": 1,
            "hint": "Creating your account at a new employer — that's enrolment. You get an ID linked to your record.",
        },
        {
            "q": "What is IAM (Identity and Access Management)?",
            "opts": {
                "A": "A firewall technology for blocking unauthorised connections",
                "B": "The collective process of authorising access to resources based on verified identity",
                "C": "A malware detection framework",
                "D": "A government framework for issuing digital passports"},
            "ans": "B", "diff": 2,
            "hint": "Think of the entire pipeline: who are you → prove it → here's what you can access.",
        },
        {
            "q": "Why are 'salted passwords' more secure than simply hashing passwords?",
            "opts": {
                "A": "Salts encrypt the hash output making it longer",
                "B": "Salts add random data before hashing so identical passwords produce different hashes, defeating rainbow tables",
                "C": "Salts replace the password entirely, removing the need for user input",
                "D": "Salts slow down the login process, making brute force impossible"},
            "ans": "B", "diff": 2,
            "hint": "Even if two users pick 'password123', with different salts their stored hashes differ completely.",
        },
        {
            "q": "Where are Windows password hashes commonly stored (the target for offline attacks)?",
            "opts": {
                "A": "C:\\Users\\[username]\\passwords.dat",
                "B": "C:\\Windows\\System32\\Config\\SAM",
                "C": "/etc/shadow equivalent in Windows",
                "D": "In the Windows Registry under HKLM\\Security\\Accounts"},
            "ans": "B", "diff": 2,
            "hint": "Security Account Manager — forensic tools can extract this file to crack hashes offline.",
        },
        {
            "q": "What is a challenge-response authentication protocol?",
            "opts": {
                "A": "A system where the server sends a random challenge that only the real user can correctly answer (prove knowledge of a secret) without revealing the secret",
                "B": "A CAPTCHA system to distinguish humans from bots",
                "C": "A process where users challenge admins to reset their accounts",
                "D": "A two-step verification using email and SMS codes"},
            "ans": "A", "diff": 2,
            "hint": "'What's 2+2?' isn't secure — but 'sign this random nonce with your private key' is.",
        },
        {
            "q": "Why are slow/expensive password hashing algorithms like bcrypt or Argon2 preferred over fast hash algorithms like SHA-256 for passwords?",
            "opts": {
                "A": "They produce longer hashes that cannot be stored in rainbow tables",
                "B": "They are computationally expensive for the attacker too — each guess takes much longer, making large-scale brute force impractical",
                "C": "They are the only algorithms approved by NIST for passwords",
                "D": "They automatically salt passwords without any configuration"},
            "ans": "B", "diff": 3,
            "hint": "If bcrypt takes 0.1s per attempt, an attacker testing billions of passwords suddenly takes years.",
        },
        {
            "q": "The module warns that 'almost all' the authentication protocols demonstrated are broken. What is the key lesson from this?",
            "opts": {
                "A": "All authentication should be biometric only",
                "B": "Authentication is an unsolved problem and no system can ever be secure",
                "C": "These examples illustrate concepts — never implement your own authentication protocols; use battle-tested libraries",
                "D": "Multi-factor authentication always compensates for protocol weaknesses"},
            "ans": "C", "diff": 3,
            "hint": "The warning is the same as with cryptography — DIY authentication is how professionals get burned.",
        },
        {
            "q": "What makes PBKDF2, bcrypt and scrypt better than a simple salted SHA-256 hash for password storage?",
            "opts": {
                "A": "They use asymmetric encryption, making the hash unrecoverable",
                "B": "They are key derivation functions designed to be computationally expensive, with tunable cost parameters to keep pace with hardware improvements",
                "C": "They encrypt the salt as well, doubling security",
                "D": "They were developed by NIST specifically for passwords"},
            "ans": "B", "diff": 3,
            "hint": "The 'cost' or 'iterations' parameter is the key — you can always make it slower as hardware improves.",
        },
        {
            "q": "If an attacker steals a salted password hash file, what attack is still possible even with a unique salt per user?",
            "opts": {
                "A": "Rainbow table lookup",
                "B": "No attack is possible with a salt",
                "C": "Targeted brute force guessing on individual accounts, using the known salt",
                "D": "Hash length extension attack"},
            "ans": "C", "diff": 3,
            "hint": "The salt is not a secret — with the salt and hash, you can still try millions of guesses for one account.",
        },
    ],

    "Module 7 – Authentication II": [
        {
            "q": "What is biometric authentication?",
            "opts": {
                "A": "Using a password known only to the user",
                "B": "Using unique physical characteristics (e.g. fingerprint, face, voice) to verify identity",
                "C": "Using a hardware token that generates one-time codes",
                "D": "Using a smartcard with a PIN"},
            "ans": "B", "diff": 1,
            "hint": "Your body IS your credential — fingerprints, face, voice, keystroke patterns.",
        },
        {
            "q": "What is a 'False Acceptance' error (Type I error) in biometric authentication?",
            "opts": {
                "A": "The system rejects the legitimate user",
                "B": "The system grants access to an impostor because their scan falls within the confidence limits",
                "C": "The sensor fails to take a reading",
                "D": "The biometric template stored on the server is corrupted"},
            "ans": "B", "diff": 1,
            "hint": "Mallory's fingerprint is close enough — the system wrongly lets her in as Rob.",
        },
        {
            "q": "What type of token can perform cryptographic operations (like digital signatures) to authenticate with a server?",
            "opts": {
                "A": "Magnetic stripe card",
                "B": "Passive RFID fob",
                "C": "Active cryptographic challenge-response token (e.g., EMV card)",
                "D": "Printed barcode ticket"},
            "ans": "C", "diff": 1,
            "hint": "Your chip-and-PIN credit card does this — the chip signs a challenge from the payment terminal.",
        },
        {
            "q": "What is the key weakness of One Time Password (OTP) tokens compared to cryptographic challenge-response tokens?",
            "opts": {
                "A": "OTP tokens are too expensive to deploy",
                "B": "OTPs can be intercepted, relayed or shared — a MitM attacker can use the OTP before it expires",
                "C": "OTP tokens require a permanent internet connection",
                "D": "OTPs only work on Windows systems"},
            "ans": "B", "diff": 2,
            "hint": "The story of the US programmer who FedEx'd his RSA token to China illustrates this perfectly.",
        },
        {
            "q": "What is a 'replay attack' in the context of biometric authentication?",
            "opts": {
                "A": "Replaying recorded login attempts to bypass lockout policies",
                "B": "Presenting a previously captured biometric sample (e.g., a printed photo of a face or a copy of a fingerprint) to defeat the sensor",
                "C": "Reusing the same password across multiple systems",
                "D": "Intercepting and replaying a TLS session"},
            "ans": "B", "diff": 2,
            "hint": "Some facial recognition systems can be fooled by holding up a printed photo — that's a replay.",
        },
        {
            "q": "What does FAR stand for in biometrics, and what does a higher FAR indicate?",
            "opts": {
                "A": "File Access Rate; more files can be accessed",
                "B": "False Acceptance Rate; a higher FAR means more impostors are incorrectly authenticated",
                "C": "Fingerprint Accuracy Rating; a higher FAR means better fingerprint matching",
                "D": "Forced Authentication Request; more authentication challenges are issued"},
            "ans": "B", "diff": 2,
            "hint": "FAR and FRR are in tension — lowering one raises the other. Calibration is the challenge.",
        },
        {
            "q": "What is the difference between a 'passive' token and an 'active' token?",
            "opts": {
                "A": "Passive tokens are physical cards; active tokens are smartphone apps",
                "B": "Passive tokens present a static ID (e.g. mag stripe); active tokens contain processing power to perform calculations or generate changing IDs",
                "C": "Passive tokens require a PIN; active tokens do not",
                "D": "Active tokens communicate via Bluetooth only; passive tokens use NFC"},
            "ans": "B", "diff": 2,
            "hint": "Your old swipe card (passive) vs. your EMV chip card or Google Authenticator (active).",
        },
        {
            "q": "Certificate-based authentication provides a key advantage over username/password. What is it?",
            "opts": {
                "A": "Certificates never expire, reducing administrative overhead",
                "B": "Certificates enable mutual authentication (both client and server verify each other) and can be easily revoked if compromised",
                "C": "Certificates are free to obtain from all CAs",
                "D": "Certificate authentication does not require any network connection"},
            "ans": "B", "diff": 3,
            "hint": "Mutual TLS — both sides present and verify certs. Revocation lists mean you can kill a compromised cert.",
        },
        {
            "q": "Why is it a major security concern that you 'can't revoke someone's face' in biometric authentication?",
            "opts": {
                "A": "Face recognition systems are too expensive to update",
                "B": "If biometric data is compromised, unlike a password you cannot change your fingerprint or face — the credential is permanently compromised",
                "C": "Facial data is not legally protected under privacy laws",
                "D": "Face recognition systems automatically expire after 5 years"},
            "ans": "B", "diff": 3,
            "hint": "You can reset a password. You cannot reset your fingerprint after a database breach.",
        },
        {
            "q": "What type of biometric authentication analyses the *way* you type — including pressure, speed, and rhythm?",
            "opts": {
                "A": "Voice print analysis",
                "B": "Signature analysis",
                "C": "Retinal scan",
                "D": "Keystroke biometrics"},
            "ans": "D", "diff": 3,
            "hint": "Used by secure online exam software to verify it's really you sitting the exam throughout.",
        },
        {
            "q": "How does a One Time Password (OTP) token stay synchronised with the authentication server?",
            "opts": {
                "A": "The token checks in with the server every 30 seconds via Bluetooth",
                "B": "Both the token and server share the same PRNG seed and use time or activation count to independently calculate the same OTP",
                "C": "The server sends the OTP to the token via SMS",
                "D": "The token downloads a new seed from the server daily"},
            "ans": "B", "diff": 3,
            "hint": "TOTP — Time-based OTP. Seed + timestamp → HMAC → truncate to 6 digits. Both sides do this independently.",
        },
        {
            "q": "What is the fundamental security advantage of cryptographic challenge-response tokens (e.g., EMV) over OTP tokens?",
            "opts": {
                "A": "Cryptographic tokens are cheaper to manufacture",
                "B": "Cryptographic tokens perform mutual authentication — the token and server verify each other — preventing MitM and relay attacks",
                "C": "Cryptographic tokens do not require a PIN",
                "D": "Cryptographic tokens store passwords locally, eliminating server-side storage risks"},
            "ans": "B", "diff": 3,
            "hint": "The server signs a challenge; the token signs a response — neither party can be impersonated by a relay.",
        },
    ],

    "Module 8 – Information Classification": [
        {
            "q": "What is 'information classification'?",
            "opts": {
                "A": "Sorting files alphabetically on a shared drive",
                "B": "Assigning appropriate levels of protection to information assets based on their sensitivity, value and risk",
                "C": "Encrypting all databases by default",
                "D": "Labelling emails as spam or not-spam"},
            "ans": "B", "diff": 1,
            "hint": "You wouldn't store your passport the same way as a newspaper — classification defines the right protection level.",
        },
        {
            "q": "What is 'Data Loss Prevention (DLP)'?",
            "opts": {
                "A": "A backup solution that prevents accidental file deletion",
                "B": "A set of tools and systems that monitor events to prevent sensitive data from being lost, misused or accessed by unauthorised users",
                "C": "A firewall rule preventing outbound connections",
                "D": "An encryption protocol for data in transit"},
            "ans": "B", "diff": 1,
            "hint": "DLP watches for sensitive data leaving the organisation — across network, storage and endpoints.",
        },
        {
            "q": "Under the Western Australia Health classification model, which category would 'patient records' fall into?",
            "opts": {"A": "Public", "B": "Protected", "C": "Confidential", "D": "Top Secret"},
            "ans": "C", "diff": 1,
            "hint": "Patient records require strong protection — they are not for public viewing.",
        },
        {
            "q": "What is the first step in classifying information according to the module?",
            "opts": {
                "A": "Assign encryption to all assets",
                "B": "Determine components and elements of the business information base (identify what information assets exist)",
                "C": "Select a DLP solution",
                "D": "Train all staff on classification policies"},
            "ans": "B", "diff": 1,
            "hint": "You can't protect what you don't know you have — step 1 is inventory.",
        },
        {
            "q": "What is the main risk of 'over-classification' of information?",
            "opts": {
                "A": "Sensitive data might be exposed to unauthorised users",
                "B": "Excessive cost and inefficiency from applying unnecessarily high levels of protection to low-sensitivity assets",
                "C": "Legal penalties for misusing classification labels",
                "D": "Staff will be unable to access information they need"},
            "ans": "B", "diff": 2,
            "hint": "Buying a $10,000 safe to store a bus ticket — the cost exceeds the value of what you're protecting.",
        },
        {
            "q": "What is the main risk of 'under-classification' of information?",
            "opts": {
                "A": "Storage costs increase unnecessarily",
                "B": "Classified information may not receive adequate protection, leading to data leaks and embarrassment",
                "C": "Staff will apply too much protection, slowing operations",
                "D": "Regulatory penalties for over-securing public data"},
            "ans": "B", "diff": 2,
            "hint": "Leaving confidential documents on a coffee table — anyone walking past could read them.",
        },
        {
            "q": "What are the three types of DLP systems mentioned in the module?",
            "opts": {
                "A": "Cloud DLP, On-premise DLP, Hybrid DLP",
                "B": "Network DLP, Storage DLP, Endpoint DLP",
                "C": "Active DLP, Passive DLP, Real-time DLP",
                "D": "Email DLP, File DLP, Database DLP"},
            "ans": "B", "diff": 2,
            "hint": "Think about where data lives and moves: the network, at rest in storage, and at the user's device.",
        },
        {
            "q": "Why should organisations 'review and re-classify information on a regular basis'?",
            "opts": {
                "A": "Regulatory bodies require annual re-classification audits by law",
                "B": "Information value and sensitivity changes over time — data that was once critical may become public, and vice versa",
                "C": "Re-classification refreshes encryption keys automatically",
                "D": "It allows the IT team to delete old data without liability"},
            "ans": "B", "diff": 2,
            "hint": "A merger announcement is confidential before it's published; after it's public, it's no longer sensitive.",
        },
        {
            "q": "Why does hardware sometimes need to be classified, not just the information it contains?",
            "opts": {
                "A": "Hardware is always more valuable than the data on it",
                "B": "Hardware may indicate organisational capabilities, contain classified material, or be used for destructive/malicious purposes if accessed by unauthorised individuals",
                "C": "Hardware classification is required by ISO standards",
                "D": "Physical assets must be insured, which requires classification"},
            "ans": "B", "diff": 3,
            "hint": "A surveillance camera in a classified area — the device itself could reveal what's being monitored.",
        },
        {
            "q": "According to the module, why don't organisations simply encrypt ALL data by default?",
            "opts": {
                "A": "Encryption is illegal for non-classified data in Australia",
                "B": "Encrypting everything involves significant trade-offs in cost, convenience and feasibility — security must be balanced with usability",
                "C": "Encryption technology cannot handle large volumes of data",
                "D": "Public data encrypted would violate freedom of information laws"},
            "ans": "B", "diff": 3,
            "hint": "If everything is treated as top-secret, the business grinds to a halt.",
        },
        {
            "q": "The module notes information classification protects more than just 'content'. What other aspects does it cover?",
            "opts": {
                "A": "Only database records and spreadsheets",
                "B": "It can protect methods, sources, and capabilities — e.g. an intelligence agency classifying HOW it collects data",
                "C": "Only electronic data, not physical documents",
                "D": "Only data that has a financial value to the organisation"},
            "ans": "B", "diff": 3,
            "hint": "A journalist protects their sources; an intelligence agency protects its collection methods, not just the intelligence.",
        },
        {
            "q": "Human curiosity is cited as a reason for maintaining proper access controls on classified information. What insight from the module supports this?",
            "opts": {
                "A": "People are always malicious and will exploit any access they have",
                "B": "If an information asset is accessible, human curiosity will drive someone to view it — even without malicious intent",
                "C": "Most insider threats come from IT administrators",
                "D": "Social engineering is ineffective against trained staff"},
            "ans": "B", "diff": 3,
            "hint": "Access control reduces both malicious and accidental exposure — curiosity doesn't require ill intent.",
        },
    ],

    "Module 9 – Malware": [
        {
            "q": "What is malware?",
            "opts": {
                "A": "A type of firewall that blocks malicious traffic",
                "B": "Software designed to infiltrate, damage or disrupt a computer system without the owner's informed consent",
                "C": "A set of security patches for operating systems",
                "D": "An intrusion detection system"},
            "ans": "B", "diff": 1,
            "hint": "MALicious softWARE — a catch-all term for anything designed to harm a system.",
        },
        {
            "q": "What is the key difference between a virus and a worm?",
            "opts": {
                "A": "Viruses target Windows; worms target Linux",
                "B": "A virus attaches itself to existing executable code to replicate; a worm actively propagates across networks on its own without needing to attach to a file",
                "C": "Worms steal data; viruses corrupt files",
                "D": "Viruses require user interaction to spread; worms cannot spread between computers"},
            "ans": "B", "diff": 1,
            "hint": "A virus needs a host file to ride in; a worm is self-propelling across networks.",
        },
        {
            "q": "What is ransomware?",
            "opts": {
                "A": "Software that displays unwanted advertisements",
                "B": "Malware that encrypts a victim's files and demands payment (usually cryptocurrency) for the decryption key",
                "C": "A type of rootkit that hides attacker activity",
                "D": "Spyware that monitors banking activity"},
            "ans": "B", "diff": 1,
            "hint": "Your files are held hostage — pay up or they stay encrypted.",
        },
        {
            "q": "What is a Trojan horse in the context of malware?",
            "opts": {
                "A": "A virus that spreads through email attachments",
                "B": "A program that appears useful or legitimate but also secretly performs malicious actions",
                "C": "Malware that replicates across a network",
                "D": "A rootkit designed to hide administrator-level access"},
            "ans": "B", "diff": 1,
            "hint": "Named after the Greek myth — it looks like a gift but contains the enemy inside.",
        },
        {
            "q": "What is a botnet?",
            "opts": {
                "A": "A network security tool for detecting intrusions",
                "B": "A collection of compromised machines (bots) controlled by a malicious actor for coordinated attacks",
                "C": "A type of firewall rule that blocks automated bots",
                "D": "A legitimate network of automated web crawlers"},
            "ans": "B", "diff": 2,
            "hint": "Robot + Network — an army of zombie computers doing the attacker's bidding.",
        },
        {
            "q": "What are the three phases of a botnet's operation?",
            "opts": {
                "A": "Scanning, Infection, Execution",
                "B": "Establishment/Recruitment, Command & Control (C2), Attack",
                "C": "Download, Install, Activate",
                "D": "Reconnaissance, Exploitation, Persistence"},
            "ans": "B", "diff": 2,
            "hint": "First build the army, then give it orders, then unleash it.",
        },
        {
            "q": "What is a rootkit?",
            "opts": {
                "A": "Malware that deletes the root directory of a file system",
                "B": "A stealthy application designed to hide the fact that an OS has been compromised, typically providing concealment, command & control, and surveillance",
                "C": "A tool for auditing root account activity on Linux systems",
                "D": "A type of ransomware targeting system files"},
            "ans": "B", "diff": 2,
            "hint": "Root (highest privilege) + kit (toolkit) — it hides the attacker's presence at the deepest level.",
        },
        {
            "q": "What is 'heuristic detection' in antivirus software?",
            "opts": {
                "A": "Matching files against a database of known malware hash signatures",
                "B": "Detecting suspicious code patterns and behaviours even when no exact signature match exists — useful against polymorphic or new malware",
                "C": "Quarantining all executable files until manually approved",
                "D": "Using machine learning to predict future attacks"},
            "ans": "B", "diff": 2,
            "hint": "If it walks like a duck and quacks like a duck — even if we've never seen THIS duck before.",
        },
        {
            "q": "What is an Advanced Persistent Threat (APT)?",
            "opts": {
                "A": "A simple automated malware scan that repeatedly targets a server",
                "B": "A well-resourced, long-term targeted attack (often state-sponsored) using sophisticated techniques against specific targets",
                "C": "A vulnerability that has been exploited for more than 6 months",
                "D": "An antivirus system that persistently monitors for advanced threats"},
            "ans": "B", "diff": 3,
            "hint": "Stuxnet — months of careful infiltration of an Iranian nuclear facility. That's an APT.",
        },
        {
            "q": "What is a 'logic bomb'?",
            "opts": {
                "A": "Malware that self-destructs after exfiltrating data",
                "B": "Code that executes a malicious action when a specific condition is met — e.g. after a payroll run or on a specific date",
                "C": "A denial of service attack using logical contradictions",
                "D": "A type of ransomware that activates based on system load"},
            "ans": "B", "diff": 3,
            "hint": "A disgruntled programmer's insurance policy — 'if I'm not in the payroll, delete everything.'",
        },
        {
            "q": "What is the 'local subnet' worm scanning strategy?",
            "opts": {
                "A": "The worm randomly probes IP addresses across the entire internet",
                "B": "A worm that has breached a host behind a firewall then scans only the local network — reaching machines that would otherwise be protected",
                "C": "The worm uses DNS lookups to find other machines in the same domain",
                "D": "The worm limits itself to scanning 10 targets per minute to avoid detection"},
            "ans": "B", "diff": 3,
            "hint": "The firewall stops outside attackers — but once one machine inside is infected, the internal network is vulnerable.",
        },
        {
            "q": "How does a 'polymorphic virus' evade antivirus signature detection?",
            "opts": {
                "A": "It encrypts itself with AES-256 so antivirus cannot read it",
                "B": "It mutates its code with every infection so that each copy has a different signature, defeating static signature matching",
                "C": "It hides in the BIOS firmware where antivirus cannot scan",
                "D": "It disables the antivirus process before scanning begins"},
            "ans": "B", "diff": 3,
            "hint": "Same intent, different disguise every time — traditional signature scanning fails here.",
        },
    ],

    "Module 10 – Application Security": [
        {
            "q": "What is the 'kernel' of an operating system?",
            "opts": {
                "A": "The graphical user interface layer",
                "B": "The heart of the OS containing all common components and managing communication between hardware and software",
                "C": "The package manager for installing applications",
                "D": "The network stack handling internet connections"},
            "ans": "B", "diff": 1,
            "hint": "Everything else in the OS is built around the kernel — it's the core.",
        },
        {
            "q": "What is the 'principle of least privilege'?",
            "opts": {
                "A": "Only senior staff should have administrator accounts",
                "B": "Applications and users should only be granted the minimum permissions needed to complete their tasks",
                "C": "All privileges should be granted by default and revoked as needed",
                "D": "Users with fewer responsibilities should have fewer login requirements"},
            "ans": "B", "diff": 1,
            "hint": "Don't run your browser as root — if it gets hacked, the blast radius is much smaller.",
        },
        {
            "q": "What is a 'Zero-Day vulnerability'?",
            "opts": {
                "A": "A vulnerability discovered on the first day of a software release",
                "B": "A previously unknown vulnerability for which no patch yet exists, giving defenders zero days of warning",
                "C": "A vulnerability rated zero in the CVSS scoring system",
                "D": "A vulnerability that has been patched but not yet deployed"},
            "ans": "B", "diff": 1,
            "hint": "The attacker knows about it; the vendor doesn't — there's zero time to patch before it's exploited.",
        },
        {
            "q": "What does OWASP stand for and what is the OWASP Top Ten?",
            "opts": {
                "A": "Open Web Application Security Project; a standard list of the most critical web application security risks",
                "B": "Official Web Audit and Security Protocol; a certification for web developers",
                "C": "Open Worldwide Application Security Platform; a commercial security tool",
                "D": "Organised Web Attack and Security Prevention; a government framework"},
            "ans": "A", "diff": 1,
            "hint": "The go-to reference for web app security — every developer should know it.",
        },
        {
            "q": "What is the 'Australian Signals Directorate Essential Eight' mitigation strategies? Name one of the eight.",
            "opts": {
                "A": "Deploy a honeypot, perform red team exercises",
                "B": "Application whitelisting, patch applications, MFA, daily backups (and 4 more)",
                "C": "Use AES-256, implement PKI, deploy IDS",
                "D": "Hire a CISO, conduct annual penetration tests, buy cyber insurance"},
            "ans": "B", "diff": 2,
            "hint": "The ASD released this list as the baseline — patch applications is one, MFA is another.",
        },
        {
            "q": "Why is the C function 'gets()' considered unsafe for application security?",
            "opts": {
                "A": "It requires root privileges to execute",
                "B": "It does not check input length, allowing attackers to overflow the buffer and overwrite adjacent memory",
                "C": "It logs user inputs to a plaintext file",
                "D": "It is deprecated and no longer compiles on modern systems"},
            "ans": "B", "diff": 2,
            "hint": "Buffer overflow 101 — gets() happily reads past the end of your buffer, corrupting memory.",
        },
        {
            "q": "What is the window of vulnerability in the context of zero-day patches?",
            "opts": {
                "A": "The time an administrator's session stays open before timeout",
                "B": "The period between when a zero-day vulnerability is discovered and when a patch is available and deployed",
                "C": "The daily window when automated scans run on the network",
                "D": "The gap between operating system updates"},
            "ans": "B", "diff": 2,
            "hint": "During this window, attackers can exploit freely with no defence available.",
        },
        {
            "q": "What is 'security instrumentation' in the context of application security?",
            "opts": {
                "A": "The tools used to perform penetration testing on applications",
                "B": "Components designed to measure, sense and monitor systems to assist with security automation, event detection and alerting",
                "C": "A set of programming libraries for building secure applications",
                "D": "The documentation of security controls for audit purposes"},
            "ans": "B", "diff": 2,
            "hint": "Think sensors — network anomaly detectors, file tripwires, log collectors. They're the security nervous system.",
        },
        {
            "q": "Why does the module argue that '100% security is not practical' even though it's theoretically possible?",
            "opts": {
                "A": "Modern hardware is too fast for any encryption to protect",
                "B": "Achieving 100% security requires removing all users, interfaces, networks and inputs — making the system completely unusable",
                "C": "Government regulations prohibit fully secure systems for national security reasons",
                "D": "100% security is actually impossible due to quantum computing"},
            "ans": "B", "diff": 3,
            "hint": "A server with no network, no users, no input, and only one output — secure but useless.",
        },
        {
            "q": "According to the module, when does software 'become insecure'?",
            "opts": {
                "A": "Only when vulnerabilities are publicly disclosed",
                "B": "All of the above — when written, when open-sourced, when new functionality is added, when vulnerabilities are discovered, etc.",
                "C": "Only when it reaches end-of-life",
                "D": "When it fails a penetration test"},
            "ans": "B", "diff": 3,
            "hint": "The question is rhetorical — the answer is 'all of the above' because security is a lifecycle, not a point in time.",
        },
        {
            "q": "What is the risk of using shared libraries (DLLs/.so files) from a security perspective?",
            "opts": {
                "A": "Shared libraries are always signed and therefore safe",
                "B": "Your application loses control — you're trusting a 'black box' that could handle dirty data insecurely or send dirty data back",
                "C": "Shared libraries increase executable size, making exploits easier",
                "D": "Shared libraries cannot be updated without recompiling all applications"},
            "ans": "B", "diff": 3,
            "hint": "You throw data into the black box — but what if the black box is compromised or poorly written?",
        },
        {
            "q": "What is a 'Critical Control Point' in the software development lifecycle for security?",
            "opts": {
                "A": "A mandatory government checkpoint before software can be sold",
                "B": "A key stage in the software lifecycle (design, development, audit, review, maintenance) where security can be verified and vulnerabilities caught",
                "C": "A network monitoring tool that intercepts critical API calls",
                "D": "A code obfuscation technique to protect intellectual property"},
            "ans": "B", "diff": 3,
            "hint": "Catching a flaw at design costs 1x; catching it in production costs 100x — control points are where you catch it early.",
        },
    ],

    "Module 11 – Privacy, Ethics & Law": [
        {
            "q": "What is Personally Identifiable Information (PII)?",
            "opts": {
                "A": "Information about the company's financial performance",
                "B": "Information that could identify a specific individual — used for identity crimes, fraud or blackmail",
                "C": "Public information published by the government",
                "D": "Technical data stored on a server"},
            "ans": "B", "diff": 1,
            "hint": "Your name, date of birth, address, Medicare number — these are PII.",
        },
        {
            "q": "Under Australian law (Criminal Code Act 1995), which of the following is a cybercrime offence?",
            "opts": {
                "A": "Using public Wi-Fi without registering your device",
                "B": "Unauthorised modification of data, including destruction of data",
                "C": "Publishing negative reviews online",
                "D": "Accessing a website more than 100 times per day"},
            "ans": "B", "diff": 1,
            "hint": "Parts 10.7 and 10.8 of the Criminal Code Act 1995 cover computer intrusion and data modification.",
        },
        {
            "q": "What are the three categories of threat actors to personal privacy discussed in the module?",
            "opts": {
                "A": "Hackers, Nation States, Corporations",
                "B": "Individuals, Commercial Organisations, Governments",
                "C": "Malware, Social Engineering, Physical Theft",
                "D": "ISPs, Social Networks, Search Engines"},
            "ans": "B", "diff": 1,
            "hint": "A thief, a data-hungry corporation, and Big Brother — three very different threats to your privacy.",
        },
        {
            "q": "What is the first principle of the ACS Code of Ethics?",
            "opts": {
                "A": "Competence",
                "B": "Honesty",
                "C": "The Primacy of the Public Interest",
                "D": "Professionalism"},
            "ans": "C", "diff": 1,
            "hint": "The public comes first — before personal, business, or sectional interests.",
        },
        {
            "q": "What is 'big data' and why does it pose a privacy concern?",
            "opts": {
                "A": "Large databases containing only financial records; concerns involve tax fraud",
                "B": "Very large datasets collected through free or commercial internet services; concerns involve context collapse, data mining and sharing with third parties without consent",
                "C": "Databases maintained by governments; concerns involve national security",
                "D": "Storage systems for multimedia content; concerns involve copyright"},
            "ans": "B", "diff": 2,
            "hint": "You give Amazon your browsing habits, and suddenly your bank knows about your lifestyle choices.",
        },
        {
            "q": "What is 'data carving' (data recovery) and why is it privacy-relevant?",
            "opts": {
                "A": "Splitting data into smaller pieces for encryption",
                "B": "Recovering data from storage media even after it has been deleted — relevant because 'deleted' data may still be recoverable",
                "C": "Carving sensitive data out of database logs",
                "D": "Partitioning a hard drive for multiple operating systems"},
            "ans": "B", "diff": 2,
            "hint": "Donating or selling an old laptop? Someone may recover your 'deleted' files with forensic tools.",
        },
        {
            "q": "What was the 'Terrorism Information Awareness' (TIA) program and what happened to it?",
            "opts": {
                "A": "A publicly-funded research program; it was completed successfully",
                "B": "A US predictive surveillance program; formally suspended by Congress in 2003 after public outcry, though its software was quietly adopted by the NSA",
                "C": "An Australian intelligence-sharing agreement; it was expanded after 9/11",
                "D": "A United Nations initiative; abandoned due to funding shortfalls"},
            "ans": "B", "diff": 2,
            "hint": "Officially dead, unofficially alive at the NSA — a cautionary tale about government surveillance.",
        },
        {
            "q": "What privacy concern does the use of free public Wi-Fi pose?",
            "opts": {
                "A": "Free Wi-Fi is always unencrypted and extremely slow",
                "B": "Free Wi-Fi operators may passively surveil users, logging browsing activity and potentially profiling users",
                "C": "Free Wi-Fi violates telecommunications law in most countries",
                "D": "Public Wi-Fi uses outdated WEP encryption that anyone can decode"},
            "ans": "B", "diff": 2,
            "hint": "Nothing is truly free — when a service is free, you are often the product.",
        },
        {
            "q": "Edward Snowden's privacy quote from the module makes an analogy. What is it?",
            "opts": {
                "A": "Saying you don't need privacy because you have nothing to hide is like saying you don't need free speech because you have nothing to say",
                "B": "Privacy is like oxygen — you only notice it when it's gone",
                "C": "Expecting privacy online is like expecting silence in a crowded room",
                "D": "Giving up privacy for security is like burning your house down to kill the rats"},
            "ans": "A", "diff": 3,
            "hint": "It connects privacy with a different, more valued right to make the point resonate.",
        },
        {
            "q": "What is the privacy risk of social networking sites according to the module?",
            "opts": {
                "A": "Social networks use weak encryption for messages",
                "B": "People publicly post their location, activities and relationships — enabling identity theft, fraud, harassment and targeted attacks",
                "C": "Social networks are owned by foreign governments",
                "D": "Social networks sell user passwords to advertisers"},
            "ans": "B", "diff": 3,
            "hint": "Why steal from someone's letterbox when their Facebook tells you they're on holiday in Bali right now?",
        },
        {
            "q": "The module highlights a key data aggregation concern: what happens when large databases are combined?",
            "opts": {
                "A": "Combined databases become too large for standard queries",
                "B": "Aggregating multiple data sources can reveal far more sensitive insights about individuals than any single source could — a privacy threat greater than the sum of its parts",
                "C": "Regulators automatically receive notification of database merges",
                "D": "Combined databases require re-encryption under GDPR"},
            "ans": "B", "diff": 3,
            "hint": "Shopping data + health app data + location data = a surprisingly intimate portrait of your life.",
        },
        {
            "q": "Why is the 'I have nothing to hide' argument against privacy considered flawed?",
            "opts": {
                "A": "Everyone has illegal activities they are hiding",
                "B": "Privacy is not about hiding wrongdoing — it is about controlling your own narrative and protecting information from being taken out of context or weaponised",
                "C": "The argument only applies to government surveillance, not corporate data collection",
                "D": "Having nothing to hide is statistically impossible given modern data collection"},
            "ans": "B", "diff": 3,
            "hint": "Your private life, out of context, becomes a weapon — the module makes this point explicitly.",
        },
    ],
}

# ── Game helpers ──────────────────────────────────────────────────────────────

def clear():
    os.system("clear" if os.name != "nt" else "cls")

def slow_print(text, delay=0.02):
    for ch in text:
        print(ch, end="", flush=True)
        time.sleep(delay)
    print()

def banner():
    clear()
    print(f"""
{BG_BLU}{WHT}{BOLD}
  ╔══════════════════════════════════════════════════════════╗
  ║         CyberQuest: Who Wants to Be a Cyber Expert?      ║
  ║              CSI6199 – Masters in Cyber Security         ║
  ╚══════════════════════════════════════════════════════════╝
{R}""")

def prize_ladder_display(current_q):
    print(f"\n{BOLD}{YLW}  ━━━━ PRIZE LADDER ━━━━{R}")
    for i in range(len(PRIZES) - 1, -1, -1):
        marker = ""
        if i == current_q:
            marker = f"  {GRN}◄ YOU ARE HERE{R}"
        elif i in SAFE_HAVENS:
            marker = f"  {CYN}✦ SAFE HAVEN{R}"
        colour = GRN if i == current_q else (CYN if i in SAFE_HAVENS else DIM)
        print(f"  {colour}{i+1:>2}. {PRIZES[i]:<10}{R}{marker}")
    print()

def format_options(opts, revealed=None):
    lines = []
    letters = ["A", "B", "C", "D"]
    for letter in letters:
        text = opts[letter]
        if revealed is not None and letter not in revealed:
            text = f"{DIM}[removed]{R}"
            lines.append(f"  {DIM}{letter}) {text}{R}")
        else:
            lines.append(f"  {BOLD}{BLU}{letter}{R}) {text}")
    return "\n".join(lines)

def ask_question(q_data, q_num, total, lifelines):
    clear()
    module_name = q_data.get("module_name", "")
    diff_labels = {1: f"{GRN}EASY{R}", 2: f"{YLW}MEDIUM{R}", 3: f"{RED}HARD{R}"}
    diff = diff_labels.get(q_data["diff"], "")

    print(f"\n{BOLD}{MGT}  Question {q_num} of {total}  {R}|  {diff}  |  {BOLD}{YLW}{PRIZES[q_num-1]}{R}")
    if module_name:
        print(f"  {DIM}({module_name}){R}")
    print()

    print(f"  {BOLD}{WHT}{q_data['q']}{R}\n")
    print(format_options(q_data["opts"]))
    print()

    # Lifelines display
    ll_display = []
    if "fifty_fifty" in lifelines:
        ll_display.append(f"{CYN}[F] 50:50{R}")
    if "hint" in lifelines:
        ll_display.append(f"{MGT}[H] Hint{R}")
    if "skip" in lifelines:
        ll_display.append(f"{YLW}[S] Skip{R}")
    ll_display.append(f"{RED}[Q] Walk away{R}")
    print(f"  Lifelines: {' | '.join(ll_display)}")
    print()

    revealed_opts = set(q_data["opts"].keys())
    used_fifty = False

    while True:
        raw = input(f"  {BOLD}Your answer (A/B/C/D or F/H/S/Q): {R}").strip().upper()

        if raw == "F" and "fifty_fifty" in lifelines:
            # Remove two wrong answers
            wrong = [k for k in q_data["opts"] if k != q_data["ans"]]
            random.shuffle(wrong)
            revealed_opts = set([q_data["ans"], wrong[0]])
            lifelines.discard("fifty_fifty")
            used_fifty = True
            clear()
            print(f"\n  {BOLD}{CYN}50:50 used! Two wrong answers removed.{R}\n")
            print(f"  {BOLD}{WHT}{q_data['q']}{R}\n")
            print(format_options(q_data["opts"], revealed_opts))
            print()
            ll_display = []
            if "hint" in lifelines:
                ll_display.append(f"{MGT}[H] Hint{R}")
            if "skip" in lifelines:
                ll_display.append(f"{YLW}[S] Skip{R}")
            ll_display.append(f"{RED}[Q] Walk away{R}")
            print(f"  Lifelines: {' | '.join(ll_display)}")
            print()
            continue

        elif raw == "H" and "hint" in lifelines:
            lifelines.discard("hint")
            print(f"\n  {BOLD}{MGT}HINT:{R} {q_data['hint']}\n")
            continue

        elif raw == "S" and "skip" in lifelines:
            lifelines.discard("skip")
            print(f"\n  {YLW}Question skipped!{R}")
            time.sleep(1)
            return "skip", lifelines

        elif raw == "Q":
            return "walkaway", lifelines

        elif raw in ("A", "B", "C", "D"):
            if used_fifty and raw not in revealed_opts:
                print(f"  {RED}That option was removed by 50:50! Choose from the remaining options.{R}")
                continue
            return raw, lifelines

        else:
            print(f"  {RED}Invalid input — enter A, B, C, D or a lifeline code.{R}")

def show_result(correct, player_ans, correct_ans, q_data):
    if correct:
        print(f"\n  {BG_GRN}{WHT}{BOLD}  ✔ CORRECT!  {R}")
        slow_print(f"\n  {GRN}{q_data['opts'][correct_ans]}{R}", 0.015)
    else:
        print(f"\n  {BG_RED}{WHT}{BOLD}  ✘ WRONG!  {R}")
        print(f"  You answered: {RED}{q_data['opts'][player_ans]}{R}")
        print(f"  Correct answer: {GRN}{q_data['opts'][correct_ans]}{R}")
    time.sleep(2.5)

def shuffle_options(q):
    """Return a shallow copy of q with answer options in a random order."""
    letters = ["A", "B", "C", "D"]
    values = [q["opts"][l] for l in letters]
    correct_value = q["opts"][q["ans"]]
    random.shuffle(values)
    new_opts = {l: v for l, v in zip(letters, values)}
    new_ans = next(l for l, v in new_opts.items() if v == correct_value)
    return {**q, "opts": new_opts, "ans": new_ans}

def select_questions(module_questions, n=12):
    """Pick n questions balanced across difficulties; fill from extras if a tier is short."""
    easy   = [q for q in module_questions if q["diff"] == 1]
    medium = [q for q in module_questions if q["diff"] == 2]
    hard   = [q for q in module_questions if q["diff"] == 3]
    for lst in (easy, medium, hard):
        random.shuffle(lst)
    selected = easy[:4] + medium[:4] + hard[:4]
    # If short, top up from leftover questions of any difficulty
    if len(selected) < n:
        used = set(id(q) for q in selected)
        extras = [q for q in module_questions if id(q) not in used]
        random.shuffle(extras)
        selected += extras[:n - len(selected)]
    return [shuffle_options(q) for q in selected[:n]]

def play_module(module_name, module_questions):
    questions = select_questions(module_questions)
    for q in questions:
        q["module_name"] = module_name

    lifelines = {"fifty_fifty", "hint", "skip"}
    safe_prize = "$0"
    score = 0

    banner()
    print(f"\n  {BOLD}{CYN}Module: {module_name}{R}")
    print(f"  {DIM}You have 3 lifelines: 50:50, Hint, and Skip.{R}")
    print(f"  {DIM}Safe havens at questions 5 and 10 — reach them to lock in a prize.{R}")
    input(f"\n  {YLW}Press ENTER to begin...{R}")

    for idx, q_data in enumerate(questions):
        q_num = idx + 1

        if idx in SAFE_HAVENS:
            safe_prize = PRIZES[idx]
            print(f"\n  {BG_YLW}{BOLD}  ★ SAFE HAVEN REACHED! ${safe_prize} is now guaranteed!  {R}")
            time.sleep(2)

        answer, lifelines = ask_question(q_data, q_num, len(questions), lifelines)

        if answer == "walkaway":
            print(f"\n  {YLW}You walked away with {safe_prize}!{R}")
            time.sleep(2)
            return score, safe_prize

        if answer == "skip":
            score += 0
            continue

        correct = (answer == q_data["ans"])
        show_result(correct, answer, q_data["ans"], q_data)

        if correct:
            score += 1
        else:
            print(f"\n  {RED}Game over for this module! You leave with {safe_prize}.{R}")
            time.sleep(2.5)
            return score, safe_prize

    # Completed all questions!
    final_prize = PRIZES[len(questions) - 1]
    print(f"\n  {BG_GRN}{WHT}{BOLD}  🏆 MODULE COMPLETE! You won {final_prize}!  {R}")
    time.sleep(2)
    return score, final_prize

def module_summary(results):
    banner()
    print(f"\n  {BOLD}{YLW}{'━'*50}{R}")
    print(f"  {BOLD}{WHT}       SESSION RESULTS{R}")
    print(f"  {BOLD}{YLW}{'━'*50}{R}\n")
    total_q = 0
    total_c = 0
    for mod, (score, questions, prize) in results.items():
        pct = int((score / questions) * 100) if questions > 0 else 0
        colour = GRN if pct >= 70 else (YLW if pct >= 50 else RED)
        print(f"  {BOLD}{mod[:45]:<45}{R}")
        print(f"    Score: {colour}{score}/{questions} ({pct}%){R}  |  Prize: {YLW}{prize}{R}\n")
        total_q += questions
        total_c += score
    overall = int((total_c / total_q) * 100) if total_q else 0
    colour = GRN if overall >= 70 else (YLW if overall >= 50 else RED)
    print(f"  {BOLD}{YLW}{'━'*50}{R}")
    print(f"  {BOLD}Overall: {colour}{total_c}/{total_q} ({overall}%){R}\n")
    if overall >= 80:
        print(f"  {GRN}{BOLD}  Excellent! You're ready for that exam! 🏆{R}")
    elif overall >= 60:
        print(f"  {YLW}{BOLD}  Good work — review your weaker modules and you'll nail it!{R}")
    else:
        print(f"  {RED}{BOLD}  Keep studying — you've identified exactly where to focus! 💪{R}")
    print()

def main_menu():
    module_names = list(MODULES.keys())
    while True:
        banner()
        print(f"  {BOLD}{WHT}Select an option:{R}\n")
        print(f"  {YLW}[0]{R} Play ALL modules (full exam simulation)")
        for i, name in enumerate(module_names, 1):
            print(f"  {YLW}[{i}]{R} {name}")
        print(f"\n  {RED}[Q]{R} Quit")
        print()
        choice = input(f"  {BOLD}Enter choice: {R}").strip().upper()

        if choice == "Q":
            print(f"\n  {CYN}Good luck on your exam! 🎓{R}\n")
            sys.exit(0)

        if choice == "0":
            results = {}
            for name in module_names:
                banner()
                print(f"\n  {BOLD}{MGT}Up next: {name}{R}")
                time.sleep(1.5)
                score, prize = play_module(name, MODULES[name])
                results[name] = (score, 12, prize)
            module_summary(results)
            input(f"  {YLW}Press ENTER to return to menu...{R}")
            continue

        try:
            idx = int(choice) - 1
            if 0 <= idx < len(module_names):
                name = module_names[idx]
                score, prize = play_module(name, MODULES[name])
                results = {name: (score, 12, prize)}
                module_summary(results)
                input(f"  {YLW}Press ENTER to return to menu...{R}")
            else:
                print(f"  {RED}Invalid choice.{R}")
                time.sleep(1)
        except ValueError:
            print(f"  {RED}Invalid choice.{R}")
            time.sleep(1)

if __name__ == "__main__":
    try:
        main_menu()
    except KeyboardInterrupt:
        print(f"\n\n  {CYN}See you next time! 🎓{R}\n")
        sys.exit(0)
