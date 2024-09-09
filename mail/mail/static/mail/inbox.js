document.addEventListener("DOMContentLoaded", function () {
	// Use buttons to toggle between views
	document
		.querySelector("#inbox")
		.addEventListener("click", () => load_mailbox("inbox"));
	document
		.querySelector("#sent")
		.addEventListener("click", () => load_mailbox("sent"));
	document
		.querySelector("#archived")
		.addEventListener("click", () => load_mailbox("archive"));
	document.querySelector("#compose").addEventListener("click", compose_email);

	document
		.querySelector("#compose-form")
		.addEventListener("submit", send_email);
	// By default, load the inbox
	load_mailbox("inbox");
});

function compose_email() {
	// Show compose view and hide other views
	document.querySelector("#emails-view").style.display = "none";
	document.querySelector("#compose-view").style.display = "block";

	// Clear out composition fields
	document.querySelector("#compose-recipients").value = "";
	document.querySelector("#compose-subject").value = "";
	document.querySelector("#compose-body").value = "";
}

function load_mailbox(mailbox) {
	// Show the mailbox and hide other views
	document.querySelector("#emails-view").style.display = "block";
	document.querySelector("#compose-view").style.display = "none";

	// Show the mailbox name
	document.querySelector("#emails-view").innerHTML = `<h3>${
		mailbox.charAt(0).toUpperCase() + mailbox.slice(1)
	}</h3>`;
	fetch(`/emails/${mailbox}`)
		.then((response) => response.json())
		.then((emails) => {
			emails.forEach((mail) => {
				const email_elements = document.createElement("div");
				email_elements.innerHTML = `
	<div class="card" id="mail-${mail.id}" style="${
					mail.read ? "background-color:lightgray" : ""
				}">
		<div class="card-body">
			<div class="row">
				<div class="col-3">
					<h6 class="card-title">${mail.sender}</h6>
				</div>
				<div class="col-6">
					<h6 class="card-title">${mail.subject}</h6>
				</div>
				<div class="col-3">
					<h6 class="card-title">${mail.timestamp}</h6>
				</div>
			</div>
		</div>
	</div>
`;

				email_elements.style.cursor = "pointer";
				email_elements.addEventListener("click", () => {
					fetch(`/emails/${mail.id}`, {
						method: "PUT",
						body: JSON.stringify({
							read: true,
						}),
					});
					load_mail(mail.id);
				});
				document.querySelector("#emails-view").appendChild(email_elements);
			});
		});
}

function load_mail(id) {
	fetch(`/emails/${id}`)
		.then((response) => response.json())
		.then((email) => {
			document.querySelector("#emails-view").innerHTML = `
	<div class="card">
		<div class="card-body">
			<h5 class="card-title">Subject: ${email.subject}</h5>
			<hr>
			<p class="card-text">${email.body}</p>
			<hr>
			<h6 class="card-title">${email.timestamp}</h6>
		</div>
	</div>
	<button id="archive_button" class="btn btn-warning btn-sm"></button>
	<button id="reply_button" class="btn btn-sm btn-primary"></button>
`;
			if (!email.read) {
				fetch(`/emails/${id}`, {
					method: "PUT",
					body: JSON.stringify({
						read: true,
					}),
				});
			}

			const reply_button = document.getElementById("reply_button");
			reply_button.innerHTML = "Reply";
			reply_button.addEventListener("click", () => {
				compose_email();
				document.querySelector("#compose-recipients").value = email.sender;
				document.querySelector("#compose-subject").value =
					email.subject.startsWith("Re:")
						? email.subject
						: `Re: ${email.subject}`;
				document.querySelector(
					"#compose-body"
				).value = `On ${email.timestamp} ${email.sender} wrote: ${email.body}`;
			});
			const archive_button = document.getElementById("archive_button");
			archive_button.innerHTML = email.archived ? "Unarchive" : "Archive";
			archive_button.addEventListener("click", () => {
				fetch(`/emails/${id}`, {
					method: "PUT",
					body: JSON.stringify({
						archived: !email.archived,
					}),
				}).then(() => load_mailbox("Archive"));
			});
			document.querySelector("#emails-view").appendChild(reply_button);
		});
}

function send_email(event) {
	event.preventDefault();
	const EMailRecipients = document.querySelector("#compose-recipients").value;
	const EMailSubject = document.querySelector("#compose-subject").value;
	const EMailBody = document.querySelector("#compose-body").value;
	fetch("/emails", {
		method: "POST",
		body: JSON.stringify({
			recipients: EMailRecipients,
			subject: EMailSubject,
			body: EMailBody,
		}),
	})
		.then((response) => response.json())
		.then((result) => {
			load_mailbox("sent");
			console.log(result);
		});
}

/* if (!email.read) {
	fetch(`/emails/${id}`, {
		method: "PUT",
		body: JSON.stringify({
			read: true,
		}),
	});
	document.getElementById(`mail-${email.id}`).style.backgroundColor =
		"lightgray";
} */
