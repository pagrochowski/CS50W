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

  document.querySelector('#compose-form').onsubmit = () => { 
    // Fetch the promise from emails route
    fetch('/emails', {
      method: 'POST',
      body: JSON.stringify({
          recipients: document.querySelector('#compose-recipients').value,
          subject: document.querySelector('#compose-subject').value,
          body: document.querySelector('#compose-body').value
      })
    })
    // Wait for the response and validate
    .then(response => {
      if (response.ok) {
        console.log("Response okay!");
        return response.json();
      }
      else {
        console.log("Response not okay, error below.");
        throw response;
      }
    })
    // Handle the result
    .then(result => {
        // Print result
        console.log(result);
        // Switch to Sent emails box
        load_mailbox('sent');
    })
    // Error catching, in case something goes wrong
    .catch(error => {
      try {
        error.json().then(err => {
          console.error('Error sending email:', err);
        })
      } catch (parseError) {
          console.error('Error parsing error response', parseError);
      }
    });
    
    // Preventing default behaviour of form submission (to see logs)
    return false;
  };

}

function load_mailbox(mailbox) {
  
  // Show the mailbox and hide other views
  document.querySelector('#emails-view').style.display = 'block';
  document.querySelector('#compose-view').style.display = 'none';

  // Show the mailbox name
  document.querySelector('#emails-view').innerHTML = `<h3>${mailbox.charAt(0).toUpperCase() + mailbox.slice(1)}</h3>`;
  
  // Dynamic fetch URL based on mailbox
  fetch(`/emails/${mailbox}`)
  .then(response => response.json())
  .then(emails => {
    // Clear any existing emails
    // document.querySelector('#emails-view').innerHTML = ''; 

    // Show the mailbox name (after clearing)
    document.querySelector('#emails-view').innerHTML = `<h3>${mailbox.charAt(0).toUpperCase() + mailbox.slice(1)}</h3>`;
    // Display the fetched emails
    emails.forEach(email => {

      const emailDiv = document.createElement('div');
      // Adding CSS class for styling
      emailDiv.classList.add('email-container'); 
      
      emailDiv.innerHTML = `
        <b>From:</b> ${email.sender} 
        <b>Subject:</b> ${email.subject}
        <span class="timestamp">${email.timestamp}</span> 
        read status: ${email.read}
        email id: ${email.id}
      `; 

      // Apply 'read' class to read emails
      if (email.read) { 
      emailDiv.classList.add('read');
      } 

      document.querySelector('#emails-view').appendChild(emailDiv);

      // Add click listener
      emailDiv.addEventListener('click', () => {
        viewEmail(email.id, emailDiv); // Pass emailId and the div itself
      });

    });
  })
  .catch(error => console.error('Error fetching emails:', error))
  
}

function viewEmail(emailId, clickedEmailDiv) {
  // Check if email details already exist for this email
  const existingDetails = clickedEmailDiv.nextElementSibling;

  if (existingDetails && existingDetails.classList.contains('email-details')) {
    // Details exist, remove them
    existingDetails.remove();
  } 
  else {
    // Fetch email details
    fetch(`/emails/${emailId}`)
        .then(response => response.json())
        .then(email => {
            const emailDetails = document.createElement('div');
            emailDetails.classList.add('email-details'); // Adding class for hiding/styling

            // Populate with email details
            emailDetails.innerHTML = `
                <div><b>From:</b> ${email.sender}</div>
                <div><b>Recipients:</b> ${email.recipients.join(', ')}</div>
                <div><b>Subject:</b> ${email.subject}</div>
                <div><b>Timestamp:</b> ${email.timestamp}</div>
                <hr>
                <div>${email.body}</div> 
            `;

            // Insert details after the clicked email div
            clickedEmailDiv.parentNode.insertBefore(emailDetails, clickedEmailDiv.nextSibling);
        })
        .catch(error => console.error('Error fetching email:', error)); 
  }
}
