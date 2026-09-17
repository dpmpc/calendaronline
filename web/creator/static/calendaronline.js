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
  img.src = imageData;

  if (cropper[id]) {
    cropper[id].destroy();
  }

  cropper[id] = enableCropper(img, id, key, aspectRatio);
  cropper[id].imageReplaced = true;
}

function parseAspectRatio(aspectRatio) {
  const parsed = parseFloat(aspectRatio);
  return Number.isFinite(parsed) && parsed > 0 ? parsed : NaN;
}

function getCropperSelection(cropperInstance) {
  if (!cropperInstance || !cropperInstance.getCropperSelection) {
    return null;
  }
  return cropperInstance.getCropperSelection();
}

function getCropperImage(cropperInstance) {
  if (!cropperInstance || !cropperInstance.getCropperImage) {
    return null;
  }
  return cropperInstance.getCropperImage();
}

function withCropperSelection(cropperInstance, callback, retries = 20) {
  const selection = getCropperSelection(cropperInstance);
  if (selection) {
    callback(selection);
    return;
  }
  if (retries > 0) {
    setTimeout(function() {
      withCropperSelection(cropperInstance, callback, retries - 1);
    }, 25);
  }
}

function buildCropperTemplate(aspectRatio) {
  const ratio = parseAspectRatio(aspectRatio);
  const initialAspectRatio = Number.isNaN(ratio) ? '' : ' initial-aspect-ratio="' + ratio + '"';

  return (
    '<cropper-canvas background>'
    + '<cropper-image rotatable scalable translatable></cropper-image>'
    + '<cropper-shade hidden></cropper-shade>'
    + '<cropper-handle action="select" plain></cropper-handle>'
    + '<cropper-selection initial-coverage="1"' + initialAspectRatio + ' movable resizable>'
    + '<cropper-grid role="grid" bordered covered></cropper-grid>'
    + '<cropper-crosshair centered></cropper-crosshair>'
    + '<cropper-handle action="move" theme-color="rgba(255, 255, 255, 0.35)"></cropper-handle>'
    + '<cropper-handle action="n-resize"></cropper-handle>'
    + '<cropper-handle action="e-resize"></cropper-handle>'
    + '<cropper-handle action="s-resize"></cropper-handle>'
    + '<cropper-handle action="w-resize"></cropper-handle>'
    + '<cropper-handle action="ne-resize"></cropper-handle>'
    + '<cropper-handle action="nw-resize"></cropper-handle>'
    + '<cropper-handle action="se-resize"></cropper-handle>'
    + '<cropper-handle action="sw-resize"></cropper-handle>'
    + '</cropper-selection>'
    + '</cropper-canvas>'
  );
}

function enableCropper(img, id, storedCropperKey, aspectRatio) {
  var storedCropperData = false
  if (storedCropperKey && localStorage.getItem(storedCropperKey)) {
    storedCropperData = JSON.parse(localStorage.getItem(storedCropperKey))
  }

  const cropperInstance = new Cropper(img, {
    template: buildCropperTemplate(aspectRatio),
  });
  const ratio = parseAspectRatio(aspectRatio);
  const adapter = {
    cropper: cropperInstance,
    imageReplaced: false,
    scaleXValue: 1,
    scaleYValue: 1,
    rotate(degrees) {
      const image = getCropperImage(this.cropper);
      if (image) {
        image.$rotate((degrees * Math.PI) / 180);
      }
    },
    scaleX(value) {
      const image = getCropperImage(this.cropper);
      if (image && this.scaleXValue !== 0) {
        image.$scale(value / this.scaleXValue, 1);
        this.scaleXValue = value;
      }
    },
    scaleY(value) {
      const image = getCropperImage(this.cropper);
      if (image && this.scaleYValue !== 0) {
        image.$scale(1, value / this.scaleYValue);
        this.scaleYValue = value;
      }
    },
    getData() {
      const selection = getCropperSelection(this.cropper);
      if (!selection) {
        return { x: 0, y: 0, width: 0, height: 0 };
      }
      return {
        x: selection.x,
        y: selection.y,
        width: selection.width,
        height: selection.height,
      };
    },
    setData(data) {
      withCropperSelection(this.cropper, function(selection) {
        const x = Number(data.x) || 0;
        const y = Number(data.y) || 0;
        const width = Number(data.width) || selection.width || 0;
        const height = Number(data.height) || selection.height || 0;
        selection.$change(x, y, width, height, ratio, true);
      });
    },
    getCroppedCanvas(options) {
      const buildCanvasPromise = new Promise((resolve) => {
        withCropperSelection(this.cropper, function(selection) {
          const width = Math.max(options.minWidth || 1, Math.min(options.maxWidth || selection.width, selection.width || 1));
          const height = Math.max(options.minHeight || 1, Math.min(options.maxHeight || selection.height, selection.height || 1));

          selection.$toCanvas({
            width: Math.round(width),
            height: Math.round(height),
          }).then(resolve);
        });
      });

      return {
        toBlob(callback, type, quality) {
          buildCanvasPromise.then((canvas) => {
            canvas.toBlob(callback, type, quality);
          });
        },
      };
    },
    replace(imageData) {
      img.src = imageData;
      const image = getCropperImage(this.cropper);
      if (image) {
        image.src = imageData;
      }
    },
    destroy() {
      this.cropper.destroy();
    }
  };

  withCropperSelection(cropperInstance, function(selection) {
    selection.addEventListener('change', function() {
      if (storedCropperKey) {
        localStorage.setItem(storedCropperKey, JSON.stringify(adapter.getData()));
      }
    });

    if (storedCropperData) {
      console.log("Restoring cropper data", storedCropperData)
      adapter.setData(storedCropperData)
    }
  });

  return adapter;
}

// Live Preview functionality
var livePreviewDebounceTimer = null;

function updateLivePreview(monthId) {
  console.log("Updating live preview for month", monthId);
  
  // Clear any pending debounce timer
  if (livePreviewDebounceTimer) {
    clearTimeout(livePreviewDebounceTimer);
  }
  
  // Debounce the preview update to avoid too many requests
  livePreviewDebounceTimer = setTimeout(function() {
    generateLivePreview(monthId);
  }, 300);
}

function generateLivePreview(monthId) {
  var container = document.getElementById('preview-container-' + monthId);
  if (!container) {
    console.error("Preview container not found for month", monthId);
    return;
  }
  
  // Show loading state
  container.innerHTML = '<div class="preview-loading"><div class="spinner-border text-light" role="status"><span class="visually-hidden">Laden...</span></div><p>Vorschau wird erstellt...</p></div>';
  
  // Collect form data for the specific month
  var formData = new FormData(document.forms['months']);
  formData.set('lenght', '1');
  formData.set('ids', monthId + ',');
  
  // Add cropped image if available
  var croppedCanvasOptions = {
    minWidth: 256,
    minHeight: 256,
    maxWidth: 2048,
    maxHeight: 2048,
  };
  
  if (cropper[monthId]) {
    var boxData = cropper[monthId].getData();
    formData.set("image_x_" + monthId, boxData['x']);
    formData.set("image_y_" + monthId, boxData['y']);
    formData.set("image_width_" + monthId, boxData['width']);
    formData.set("image_height_" + monthId, boxData['height']);
    
    // Get cropped canvas and convert to blob
    cropper[monthId].getCroppedCanvas(croppedCanvasOptions).toBlob(function(blob) {
      formData.append('image_' + monthId, blob, 'image_' + monthId + '.jpeg');
      sendPreviewRequest(formData, container, monthId);
    }, 'image/jpeg', 0.8);
  } else {
    // No image selected, send request without image
    sendPreviewRequest(formData, container, monthId);
  }
}

function sendPreviewRequest(formData, container, monthId) {
  var xhr = new XMLHttpRequest();
  xhr.open("POST", "create", true);
  xhr.responseType = 'blob';
  
  xhr.onload = function() {
    if (xhr.status === 200) {
      // Create object URL for the PDF blob
      var pdfUrl = window.URL.createObjectURL(xhr.response);
      
      // Create an embedded PDF viewer using an object/embed element
      container.innerHTML = '<object data="' + pdfUrl + '" type="application/pdf" width="100%" height="500px" style="background: white;"><p>PDF Vorschau kann nicht angezeigt werden. <a href="' + pdfUrl + '" target="_blank">PDF herunterladen</a></p></object>';
      
      console.log("Live preview generated successfully for month", monthId);
    } else {
      console.error("Preview generation failed with status", xhr.status);
      container.innerHTML = '<div class="preview-placeholder"><span class="fa fa-exclamation-triangle"></span><p>Vorschau konnte nicht erstellt werden.<br>Bitte versuchen Sie es erneut.</p></div>';
    }
  };
  
  xhr.onerror = function() {
    console.error("Network error during preview generation");
    container.innerHTML = '<div class="preview-placeholder"><span class="fa fa-exclamation-triangle"></span><p>Netzwerkfehler.<br>Bitte überprüfen Sie Ihre Verbindung.</p></div>';
  };
  
  xhr.send(formData);
}