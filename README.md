
# react-native-ftp

## Getting started

`$ npm install react-native-ftp --save`

### Mostly automatic installation

`$ react-native link react-native-ftp`

### Manual installation

#### Android

1. Open up `android/app/src/main/java/[...]/MainActivity.java`
  - Add `import com.reactlibrary.RNFtpPackage;` to the imports at the top of the file
  - Add `new RNFtpPackage()` to the list returned by the `getPackages()` method
2. Append the following lines to `android/settings.gradle`:
  	```
  	include ':react-native-ftp'
  	project(':react-native-ftp').projectDir = new File(rootProject.projectDir, 	'../node_modules/react-native-ftp/android')
  	```
3. Insert the following lines inside the dependencies block in `android/app/build.gradle`:
  	```
      compile project(':react-native-ftp')
  	```

## Usage
```javascript
import FTP from 'react-native-ftp';

// TODO: What to do with the module?
FTP.setup("192.168.1.1",21) //Setup host
FTP.login("username","password").then(
  (result)=>{
    FTP.list(".").then(
      (result)=>{
        console.log(result);
      }
    );
  },
  (error)=>{
    alert(error);
  }
)

```
