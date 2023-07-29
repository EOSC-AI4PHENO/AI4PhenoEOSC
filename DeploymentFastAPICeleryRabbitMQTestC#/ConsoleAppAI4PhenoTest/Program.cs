// See https://aka.ms/new-console-template for more information

using ConsoleAppAI4PhenoTest;

Ticket objtaskTicket1 = ImageWellExposedTest.PostSunriseSunsetCall();
SunriseSunsetOutput objSunriseSunsetOutput=ImageWellExposedTest.GetSunriseSunsetCallResult(objtaskTicket1.task_id);

//Ticket objtaskTicket2 = ImageWellExposedTest.PostisImageWellExposedByHistoCall();
//ImageWellExposedOutput objImageWellExposedOutput = ImageWellExposedTest.GetisImageWellExposedByHistoCallResult(objtaskTicket2.task_id);

//Ticket objtaskTicket3 = AppleSegmentationTest.PostAppleSegmentationGetAppleAutomaticRoisCall();
//AutomaticAppleSegmentationOutput objAutomaticAppleSegmentationOutput = AppleSegmentationTest.GetAppleSegmentationGetAppleAutomaticRoisCallResult("00b9b9c8-a0fc-4588-979b-406b63e534b4");