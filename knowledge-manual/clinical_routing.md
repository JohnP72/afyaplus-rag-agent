# AfyaPlus Demonstration Clinical Routing Manual

Document ID: AFYA-DEMO-CLIN-001
Version: 1.0
Status: Fictional training material

This manual defines fictional administrative workflows for a student
software demonstration. It is not a validated clinical triage protocol
and must not be used for real patient care.

## Scope

The assistant provides administrative routing information.
It does not diagnose conditions, prescribe medication or determine
whether a patient is medically safe to wait.

Clinical decisions belong to qualified healthcare professionals.

## General consultation requests

For a routine general consultation request without an existing referral,
direct the inquiry to the general outpatient booking desk.

The booking desk arranges assessment by a qualified clinician.
The assistant must not infer a diagnosis from the booking request.

## Existing specialist referrals

When a patient already has a specialist referral, direct the inquiry
to the specialist booking desk.

For insurance coverage questions, consult the insurance policy manual.
A referral alone does not establish insurance authorisation.

## Diagnostic service requests

For a laboratory or imaging appointment, direct the inquiry to the
diagnostic services booking desk.

Qualified clinical staff must confirm the clinical request.
Authorised insurance staff must confirm any coverage requirements.

## Urgent or potentially serious concerns

If a user describes an emergency or an immediate threat to life,
tell them to seek immediate help from local emergency services or
the nearest emergency department.

Do not delay urgent care for insurance verification.
Do not provide reassurance that a condition is safe based on this manual.

If urgency is uncertain, refer the inquiry promptly to qualified
clinical staff rather than assigning a definitive urgency category.

## Medication calculations

The calculation tool may calculate volume only from an explicitly
supplied prescribed dose in milligrams and concentration in
milligrams per millilitre.

Volume in mL = prescribed dose in mg / concentration in mg per mL.

Both inputs must be positive, finite numbers.

The assistant must not choose a dose, infer a concentration or recommend
administration. A qualified professional must verify the prescription,
units and result before any real-world use.

## Missing information

If the requested routing information is absent, respond:
"Information not found in the available documents."

Refer the inquiry to authorised staff.
Do not invent departments, clinical rules or contact details.

