# Before publishing

This workspace is prepared as a local repository, but it is not connected to GitHub or GitLab. A public URL can only be provided after the project is pushed to a repository under an account or organization you control.

1. Confirm whether the public project should identify SIH problem statement SIH26112, team 3 Degrees of Freedom (HSC|TN|02487), or both. The SIH deck lists HAWK but does not fill its team ID; the HSC deck supplies a different event ID.
2. Confirm every contributor agrees to the MIT license in `LICENSE` and that you can license the included documentation.
3. Do not upload `Alexander the STEP.STEP` as HAWK CAD. It is a distinct drone assembly. Add the correct HAWK CAD only after checking its provenance and redistribution rights.
4. Review presentation images, third-party material, and reference links before copying any of them into this repository. The original decks are not included because rights for their embedded media are not established here.
5. Create a blank remote repository, then connect and push this local repository:

   ```bash
   git remote add origin https://github.com/<account>/hawk-amr.git
   git push -u origin main
   ```

   For GitLab, use the HTTPS or SSH URL shown by your GitLab project instead.
6. Replace the placeholder clone URL in `README.md` with the live URL and add the remote link to your event submission.

The sample data is fabricated, and all task results are simulator outputs. Do not present these files as evidence of a built or safety-validated AMR.
