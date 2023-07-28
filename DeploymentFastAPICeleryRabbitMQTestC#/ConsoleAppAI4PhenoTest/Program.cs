// See https://aka.ms/new-console-template for more information

using ConsoleAppAI4PhenoTest;

Ticket objtaskTicket1 = ImageWellExposedTest.PostSunriseSunsetCall();
//SunriseSunsetOutput objSunriseSunsetOutput=ImageWellExposedTest.GetSunriseSunsetCallResult(objtaskTicket1.task_id);

Ticket objtaskTicket2 = ImageWellExposedTest.PostisImageWellExposedByHistoCall();
//ImageWellExposedOutput objImageWellExposedOutput = ImageWellExposedTest.GetisImageWellExposedByHistoCallResult(objtaskTicket2.task_id);

Ticket objtaskTicket3 = AppleSegmentationTest.PostAppleSegmentationGetAppleAutomaticRoisCall();
//AutomaticAppleSegmentationOutput objAutomaticAppleSegmentationOutput = AppleSegmentationTest.GetAppleSegmentationGetAppleAutomaticRoisCallResult("af81773b-fe3d-455f-aefb-48f30b1d165c");