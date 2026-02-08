function showTab(name) {
  var monthTabTrigger = document.getElementById(name);
  if (monthTabTrigger != null) {
    var tab = new bootstrap.Tab(monthTabTrigger)
    tab.show()
  }
}

function selectImage(id, aspectRatio) {
  input = document.createElement("input");
  input.type = 'file';
  input.accept="image/*";
  input.onchange = function() { updatePreview(input, id, aspectRatio) }
  input.click();
}

function addEvent(monthId, date, text, isHoliday) {
  let eventId = "-" + monthId + '-' + globalAppointmentId++;
  const list = document.getElementById("events-group-" + monthId);

  var div = document.createElement('div');
  div.setAttribute('id', 'event' + eventId)
  div.classList.add("input-group")

  var label1 = document.createElement('span');
  label1.append("Datum");
  label1.classList.add("input-group-text")

  var label2 = document.createElement('span');
  label2.append("Beschreibung");
  label2.classList.add("input-group-text")

  var label3 = document.createElement('span');
  label3.append("Feiertag");
  label3.classList.add("input-group-text")

  var inputDate = document.createElement('input');
  inputDate.classList.add("form-control")
  inputDate.setAttribute('type', 'date')
  inputDate.setAttribute('name', 'event-date_' + monthId)
  inputDate.value = date

  var inputText = document.createElement('input')
  inputText.classList.add("form-control")
  inputText.setAttribute('type', 'text')
  inputText.setAttribute('name', 'event-text_' + monthId)
  inputText.value = text

  /*
  var bankHoliday = document.createElement('div')
  bankHoliday.classList.add("input-group-text")

  var bankHolidayCheck = document.createElement('input')
  bankHolidayCheck.classList.add("form-check-input")
  bankHolidayCheck.classList.add("mt-0")

  bankHolidayCheck.setAttribute('type', 'checkbox')
  bankHolidayCheck.setAttribute('name', 'event-holiday')
  bankHolidayCheck.checked = isHoliday

  bankHoliday.append(bankHolidayCheck)
  */


  var deleteButton = document.createElement('button')
  deleteButton.classList.add("btn")
  deleteButton.classList.add("btn-danger")
  deleteButton.title = "Termin löschen"
  deleteButton.onclick = () => div.remove()

  var deleteIcon = document.createElement('span');
  deleteIcon.classList.add("fa")
  deleteIcon.classList.add("fa-calendar-minus")

  deleteButton.append(deleteIcon)
  div.append(label1)
  div.append(inputDate)
  div.append(label2)
  div.append(inputText)
  div.append(deleteButton)
  list.append(div)

}

// Global variable to store the upload modal instance
var uploadModalInstance = null;
var uploadModalReady = false;

function uploadImages(saveProject) {
  console.log("Starting uploadImages", saveProject);
  
  // Open the modal programmatically and store the instance
  var modalEl = document.getElementById('upload-images-modal');
  uploadModalInstance = bootstrap.Modal.getOrCreateInstance(modalEl);
  
  // Wait for modal to be fully shown before marking as ready
  uploadModalReady = false;
  modalEl.addEventListener('shown.bs.modal', function() {
    console.log("Modal is now fully shown and ready");
    uploadModalReady = true;
  }, { once: true });
  
  uploadModalInstance.show();
  
  var formData = new FormData(document.forms['months']);
  formData.set('save_project', saveProject ? '1' : '0')
  var croppedCanvasOptions = {
    minWidth: 256,
    minHeight: 256,
    maxWidth: 4096,
    maxHeight: 4096,
  };
  var xhr = new XMLHttpRequest();
  xhr.open("POST", "create", true);
  xhr.responseType = 'blob';
  
  xhr.onload = function() {
    if (xhr.status == 200) {
      if (saveProject) {
        showBlob(xhr.response, "kalender.calendaronline")
      }
      else {
        showBlob(xhr.response, "kalender.pdf")
      }
      closeModal("upload-images-modal")   
    } else {
      console.error("Hochladen der Bilder ist mit Status " + xhr.status + " fehlgeschlagen:", xhr.response);
      var modalBody = document.querySelector('#upload-images-modal .modal-body');
      modalBody.innerHTML = '<div class="alert alert-danger" role="alert">Hochladen der Bilder ist fehlgeschlagen! Bitte versuchen Sie es erneut.</div>';
    }
  };

  xhr.onerror = function() {
    console.error("Netzwerkfehler beim Hochladen der Bilder");
    var modalBody = document.querySelector('#upload-images-modal .modal-body');
    modalBody.innerHTML = '<div class="alert alert-danger" role="alert">Netzwerkfehler beim Hochladen der Bilder. Bitte überprüfen Sie Ihre Internetverbindung und versuchen Sie es erneut.</div>';
  };

  xhr.upload.onprogress = function(event) {
    var progress = Math.round(event.loaded / event.total * 100);
    console.log("XHR progress", progress);
    var x=document.querySelector('.progress-bar');
    x.style.width = progress + "%";
    x.innerHTML = progress < 99 ? progress+" %" : "Verarbeite...";
  };

  var expectedBlobs = 0;
  for (month of months) {
    if (cropper[month]) expectedBlobs++;
  }

  console.log("About to create " + expectedBlobs + " blobs...")

  if (expectedBlobs > 0) {
    for (month of months) {
      if (cropper[month]) {
        console.log("Creating blob for month " + month)
        var boxData = cropper[month].getData()
        console.log("Crop Box Data for month " + month, boxData)

        formData.set("image_x_" + month, boxData['x'])
        formData.set("image_y_" + month, boxData['y'])
        formData.set("image_width_" + month, boxData['width'])
        formData.set("image_height_" + month, boxData['height'])
        const imageName = 'image_' + month;
        
        cropper[month].getCroppedCanvas(croppedCanvasOptions).toBlob((blob) => {
          formData.append(imageName, blob, imageName + '.jpeg');

          if (expectedBlobs-- <= 1) {
            console.log("Submitting xhr");
            xhr.send(formData);
          }
        }, 'image/jpeg');
      }
    }
  }
  else {
    xhr.send(formData);
  }
}

function closeModal(modalId, onClosed) {
  console.log("Closing modal with Id " + modalId);
  
  // Function to actually hide the modal
  var hideModal = function() {
    if (uploadModalInstance) {
      console.log("Calling modal.hide() on stored instance");
      uploadModalInstance.hide();
      
      // Add event listener for when modal is fully hidden
      var modalEl = document.getElementById(modalId);
      if (modalEl) {
        modalEl.addEventListener('hidden.bs.modal', event => {
          console.log("Modal with Id " + modalId + " is now hidden");
          if (onClosed) onClosed();
        }, { once: true });
      }
    } else {
      console.log("No stored modal instance available");
    }
  };
  
  // Wait for modal to be ready before hiding
  if (!uploadModalReady && uploadModalInstance) {
    console.log("Modal not ready yet, waiting for shown.bs.modal event");
    var modalEl = document.getElementById(modalId);
    modalEl.addEventListener('shown.bs.modal', function() {
      console.log("Modal is now shown, proceeding to hide");
      uploadModalReady = true;
      hideModal();
    }, { once: true });
  } else {
    // Modal is ready or already shown, hide immediately
    hideModal();
  }
}

function showBlob(blob, filename) {
  var a = document.createElement('a');
  a.href = window.URL.createObjectURL(blob);
  a.download = filename;
  a.dispatchEvent(new MouseEvent('click'));
}

function updatePreview(input, id, aspectRatio) {
  let file = input.files[0];
  let key = "{{ format }}-" + file.name + "-" + file.size
  let reader = new FileReader();
  reader.readAsDataURL(file);
  reader.onload = function () {
    setCropperImage(id, aspectRatio, key, reader.result)
  }
}

function setCropperImage(id, aspectRatio, key, imageData) {
  let img = document.getElementById("image-preview-" + id);

  if (cropper[id]) {
    cropper[id].destroy();
  }

  cropper[id] = enableCropper(img, id, key, aspectRatio);
  cropper[id].imageReplaced = true;
  cropper[id].replace(imageData);
}

function enableCropper(img, id, storedCropperKey, aspectRatio) {
  var storedCropperData = false
  if (storedCropperKey && localStorage.getItem(storedCropperKey)) {
    storedCropperData = JSON.parse(localStorage.getItem(storedCropperKey))
  }

  return new Cropper(img, {
    dragMode: 'move',
    aspectRatio: aspectRatio,
    autoCropArea: 1.0,
    viewMode: 2,
    restore: false,
    rotatable: true,
    crop(event) {
      localStorage.setItem(storedCropperKey, JSON.stringify(this.cropper.getData(true)));
    },
    ready() {
      if (this.cropper.imageReplaced && storedCropperData) {
        console.log("Restoring cropper data", storedCropperData)
        this.cropper.setData(storedCropperData)
      }
    }
  })
}