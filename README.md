# Action sign-and-noratize

Allows to sign files on MacOS using the signtool and codesign tools. 
It also allows to notarize files on MacOS using the altool tool.

Usage in your workflow (sign and notarize all the files in the install folder):

```
- name: Sign and notarize portables
  uses: alemuntoni/sign-and-notarize@v1
  with:
    input-path: 'install/*'
    input-path-2: 'install2/*' # optional
    macos-certificate: '${{ secrets.MACOS_CERTIFICATE }}' # optional
    macos-certificate-id: '${{ secrets.MACOS_CERT_ID }}' # optional
    macos-certificate-password: '${{ secrets.MACOS_CERTIFICATE_PSSW }}' # optional
    macos-notarization-team: '${{ secrets.MACOS_NOTARIZATION_TEAM_ID }}' # optional
    macos-notarization-user: '${{ secrets.MACOS_NOTARIZATION_USER }}' # optional
    macos-notarization-password: '${{ secrets.MACOS_NOTARIZATION_PSSW }}' # optional
```

It will sign and notarize all the files in the input-path that can be signed and notarized.
The input-path-2 is optional and can be used to sign and notarize more files.

## Sign on MacOS

To sign files on MacOS you need to have a certificate , its password and a certificate id, that you should store in your secrets.

```
- name: Sign and notarize portables
  uses: alemuntoni/sign-and-notarize@v1
  with:
    input-path: 'install/myApp.app'
    macos-certificate: '${{ secrets.MACOS_CERTIFICATE }}'
    macos-certificate-id: '${{ secrets.MACOS_CERT_ID }}'
    macos-certificate-password: '${{ secrets.MACOS_CERTIFICATE_PSSW }}'
```

The action will be executed only on macOS runners, and will only sign the files that match the input path.

## Notarize on MacOS

To notarize files on MacOS you need to have a notarization user , its password, and a notarization team id, that you should store in your secrets.

```
- name: Sign and notarize portables
  uses: alemuntoni/sign-and-notarize@v1
  with:
    input-path: 'install/myApp.app'
    macos-notarization-team: '${{ secrets.MACOS_NOTARIZATION_TEAM_ID }}'
    macos-notarization-user: '${{ secrets.MACOS_NOTARIZATION_USER }}'
    macos-notarization-password: '${{ secrets.MACOS_NOTARIZATION_PSSW }}'
```

The action will be executed only on macOS runners, and will only notarize the files that match the input path.

## Sign and Notarize on MacOS

To both sign and notarize, all the required secrets should be provided.

```
- name: Sign and notarize portables
  uses: alemuntoni/sign-and-notarize@v1
  with:
    input-path: 'install/myApp.app'
    macos-certificate: '${{ secrets.MACOS_CERTIFICATE }}'
    macos-certificate-id: '${{ secrets.MACOS_CERT_ID }}'
    macos-certificate-password: '${{ secrets.MACOS_CERTIFICATE_PSSW }}'
    macos-notarization-team: '${{ secrets.MACOS_NOTARIZATION_TEAM_ID }}'
    macos-notarization-user: '${{ secrets.MACOS_NOTARIZATION_USER }}'
    macos-notarization-password: '${{ secrets.MACOS_NOTARIZATION_PSSW }}'
```

The action will be executed only on macOS runners, and will only sign and notarize the files that match the input path.