function runImportantQuiz() {
    let score = 0;

    const questions = [
        ["Who should you share your OTP with? (a/b/c/d)\n a) Bank staff\n b) Family \n c) Police \n d) No one", "d"],
        ["Website must start with? a) http  b) https", "b"],
        ["A call asking OTP from bank is fraud — what to do? (a/b)\n a) Tell OTP\n b) Block the number", "b"],
        ["Cyber fraud helpline number?\n a) 1930\n b) 100", "a"],
        ["Where to report online fraud?\n a) cybercrime.gov.in\n b) Instagram", "a"],
        ["Strong password?\n a) 12345\n b) My@Secure2025", "b"],
        ["Phishing is?\n a) Fake link to steal data\n b) Online Game", "a"],
        ["Cyber harassment response?\n a) Ignore\n b) Collect proof, block & report", "b"]
    ];

    for (let i = 0; i < questions.length; i++) {
        let answer = prompt(questions[i][0]);
        if (answer && answer.toLowerCase().includes(questions[i][1])) {
            score++;
        }
    }

    document.getElementById("quizResult").innerHTML =
        "✔ Your Score: " + score + " / " + questions.length;
}
