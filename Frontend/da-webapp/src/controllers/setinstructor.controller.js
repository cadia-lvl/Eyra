/*
Copyright 2016 Matthias Petursson
Apache 2.0
*/

(function () {
'use strict';

angular.module('daApp')
.controller('SetInstructorController', SetInstructorController);

SetInstructorController.$inject = [ '$location', 
                                    '$rootScope',
                                    '$scope', 
                                    'dataService', 
                                    'deliveryService', 
                                    'localDbMiscService', 
                                    'logger',
                                    'utilityService'];

function SetInstructorController($location, $rootScope, $scope, dataService, deliveryService, localDbMiscService, logger, utilityService) {
  var setiCtrl = this;
  var dbService = localDbMiscService;
  var delService = deliveryService;
  var util = utilityService;
  
  setiCtrl.submit = submit;

  setiCtrl.name = '';
  setiCtrl.email = '';
  setiCtrl.phone = '';
  setiCtrl.address = '';
  setiCtrl.msgs = []; // error msgs from validation

  $rootScope.isLoaded = true;


  //////////

  function submit() {
    validateInputs(); // currently empty function
    if (setiCtrl.msgs.length === 0) {
      var instructorData;
      if (setiCtrl.name !== '' && setiCtrl.email !== '') {
        instructorData = {  'name':setiCtrl.name,
                            'email':setiCtrl.email,
                            'phone':(setiCtrl.phone || ''),
                            'address':(setiCtrl.address || '')};
      } else {
        // special submit by ID for existing instructors
        instructorData = {'id':(setiCtrl.instructorId || 1)};
      }
      delService.submitInstructor(instructorData).then(
        function success(response){
          try {
            var instructorId = response.data.instructorId;
            if (instructorId) {
              dataService.set('instructorId', instructorId); // set it in ram
              dbService.setInstructorId(instructorId) // set it in local db
                .then(angular.noop, util.stdErrCallback);

              alert('Instructor submitted to database!');

              $location.path('/main');
            } else {
              $scope.msg = 'Something went wrong.';
            }
          } catch (e) {
            logger.error(e);
          }
        },
        function error(response){
          $scope.msg = 'Error submitting instructor data.';
          logger.error(response);
        }
      );
    }
  }

  // sets/removes from setiCtrl.msgs with all validation errors.
  function validateInputs() {
    // not sure we want to do anything here
    // ideally we would whitelist only letters, spaces for name
    // and letters, spaces and numbers for address, but if this should
    // work for any language, that's not going to be pretty regex.

    // the only secure sanitation has to be done on server side anyway.
    // validation here would only be for user comfort, nicer error msgs etc.
    return;
  }
}
}());
