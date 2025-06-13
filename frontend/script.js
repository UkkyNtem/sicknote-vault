function verifyNote() {
    const noteId = document.getElementById('noteId').value;
    const resultDiv = document.getElementById('result');
  
    if (!noteId) {
      resultDiv.innerText = "Please enter a note ID.";
      return;
    }
  
    fetch(`https://ipraf9p9ua.execute-api.us-east-1.amazonaws.com/prod/verify?note_id=${noteId}`)
      .then(response => response.json())
      .then(data => {
        if (data.note_url) {
          resultDiv.innerHTML = `
            <p><strong>Note Found!</strong></p>
            <p>Patient Name: ${data.patient_name}</p>
            <p>Date: ${data.timestamp}</p>
            <a href="${data.note_url}" target="_blank">Download Note</a>
          `;
        } else {
          resultDiv.innerText = data.message || "Note not found.";
        }
      })
      .catch(error => {
        console.error(error);
        resultDiv.innerText = "Error verifying note.";
      });
  }
  
  function uploadNote() {
    const patientName = document.getElementById('patientName').value;
    const patientEmail = document.getElementById('patientEmail').value;
    const doctorName = document.getElementById('doctorName').value;
    const noteFile = document.getElementById('noteFile').files[0];
    const uploadResult = document.getElementById('uploadResult');
  
    if (!patientName || !patientEmail || !doctorName || !noteFile) {
      uploadResult.innerText = "Please fill in all fields and upload a PDF.";
      return;
    }
  
    const reader = new FileReader();
    reader.onload = function () {
      const base64PDF = reader.result.split(',')[1];
  
      const payload = {
        patient_name: patientName,
        patient_email: patientEmail,
        doctor_name: doctorName,
        note_file: base64PDF
      };
  
      fetch("https://ipraf9p9ua.execute-api.us-east-1.amazonaws.com/prod/upload", {
        method: "POST",
        headers: {
          "Content-Type": "application/json"
        },
        body: JSON.stringify(payload)
      })
        .then(response => response.json())
        .then(data => {
          uploadResult.innerText = data.message || "Note uploaded successfully!";
        })
        .catch(error => {
          console.error(error);
          uploadResult.innerText = "Error uploading note.";
        });
    };
  
    reader.readAsDataURL(noteFile);
  }
  