document.addEventListener('DOMContentLoaded', function() {

  // Use buttons to toggle between views
  document.querySelector('#inbox').addEventListener('click', () => load_mailbox('inbox'));
  document.querySelector('#sent').addEventListener('click', () => load_mailbox('sent'));
  document.querySelector('#archived').addEventListener('click', () => load_mailbox('archive'));
  document.querySelector('#compose').addEventListener('click', compose_email);

  // By default, load the inbox
  load_mailbox('inbox');
});

function compose_email() {

  // Show compose view and hide other views
  document.querySelector('#emails-view').style.display = 'none';
  document.querySelector('#compose-view').style.display = 'block';

  // Clear out composition fields
  document.querySelector('#compose-recipients').value = '';
  document.querySelector('#compose-subject').value = '';
  document.querySelector('#compose-body').value = '';
}

function load_mailbox(mailbox) {
  
  // Show the mailbox and hide other views
  document.querySelector('#emails-view').style.display = 'block';
  document.querySelector('#compose-view').style.display = 'none';

  // Show the mailbox name
  document.querySelector('#emails-view').innerHTML = `<h3>${mailbox.charAt(0).toUpperCase() + mailbox.slice(1)}</h3>`;
  fetch(`/emails/${mailbox}`) 
  .then(response => response.json())
  .then(emails => {
    emails.forEach(mail => {
      const email_elements = document.createElement('div');
      email_elements.innerHTML = `
        <div class="card">
          <div class="card-body">
            <div class="row">
              <div class="col-3">
                <h5 class="card-title">${mail.sender}</h5>
              </div>
              <div class="col-6">
                <h5 class="card-title">${mail.subject}</h5>
              </div>
              <div class="col-3">
                <h5 class="card-title">${mail.timestamp}</h5>
              </div>
            </div>
          </div>
        </div>
      `;
      document.querySelector('#emails-view').appendChild(email_elements);
    });
});
}

document.querySelector("#compose-form").addEventListener("submit", send_email);

function send_email(event) {
  event.preventDefault();
  const EMailRecipients = document.querySelector('#compose-recipients').value;
  const EMailSubject = document.querySelector('#compose-subject').value;
  const EMailBody = document.querySelector('#compose-body').value;
  fetch('/emails', {
    method: 'POST',
    body: JSON.stringify({
      recipients: EMailRecipients,
      subject: EMailSubject,
      body: EMailBody
    })
  })
  .then(response => response.json())
  .then(result => {
    load_mailbox('sent');
    console.log(result);
  });
}
