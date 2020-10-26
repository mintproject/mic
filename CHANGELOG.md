# Changelog

## [1.3.4](https://github.com/mintproject/mic/tree/1.3.4) (2020-09-15)

[Full Changelog](https://github.com/mintproject/mic/compare/1.3.3...1.3.4)

**Implemented enhancements:**

- mintproject/generic:latest is not up to date [\#287](https://github.com/mintproject/mic/issues/287)

**Fixed bugs:**

- files with hyphen in yaml causes issues with run [\#293](https://github.com/mintproject/mic/issues/293)
- Param auto detector will detect "multiple words in quotes" as several parameters [\#290](https://github.com/mintproject/mic/issues/290)
- String parameters in commands fail in components due to extra quotes. [\#288](https://github.com/mintproject/mic/issues/288)

**Merged pull requests:**

- Executables file [\#304](https://github.com/mintproject/mic/pull/304) ([mosoriob](https://github.com/mosoriob))
- Fix: inputs bug for SWAT model [\#303](https://github.com/mintproject/mic/pull/303) ([Cmheidelberg](https://github.com/Cmheidelberg))
- Fix: start thinks mic dir exists every time [\#297](https://github.com/mintproject/mic/pull/297) ([Cmheidelberg](https://github.com/Cmheidelberg))
- Fix: replace hyphens with underscore for yaml input direcory names [\#295](https://github.com/mintproject/mic/pull/295) ([Cmheidelberg](https://github.com/Cmheidelberg))

## [1.3.3](https://github.com/mintproject/mic/tree/1.3.3) (2020-08-03)

[Full Changelog](https://github.com/mintproject/mic/compare/1.3.2...1.3.3)

**Fixed bugs:**

- MIC is not working in WINDOWS [\#266](https://github.com/mintproject/mic/issues/266)

**Merged pull requests:**

- Develop [\#294](https://github.com/mintproject/mic/pull/294) ([mosoriob](https://github.com/mosoriob))
- Fix: use shlex instead of split by space to keep quoted strings [\#291](https://github.com/mintproject/mic/pull/291) ([Cmheidelberg](https://github.com/Cmheidelberg))
- Windowsfix [\#281](https://github.com/mintproject/mic/pull/281) ([Cmheidelberg](https://github.com/Cmheidelberg))

## [1.3.2](https://github.com/mintproject/mic/tree/1.3.2) (2020-07-28)

[Full Changelog](https://github.com/mintproject/mic/compare/1.3.1...1.3.2)

**Fixed bugs:**

- start command fails with python [\#285](https://github.com/mintproject/mic/issues/285)

**Merged pull requests:**

- fix: convert CRLF to LF [\#286](https://github.com/mintproject/mic/pull/286) ([mosoriob](https://github.com/mosoriob))
- Windowsfix [\#283](https://github.com/mintproject/mic/pull/283) ([Cmheidelberg](https://github.com/Cmheidelberg))
- Revert "Windowsfix" [\#282](https://github.com/mintproject/mic/pull/282) ([mosoriob](https://github.com/mosoriob))

## [1.3.1](https://github.com/mintproject/mic/tree/1.3.1) (2020-07-27)

[Full Changelog](https://github.com/mintproject/mic/compare/1.3.0...1.3.1)

**Fixed bugs:**

- If the requerimients.txt contains uninstallable packages, mic fails [\#284](https://github.com/mintproject/mic/issues/284)

**Closed issues:**

- Synchronize MIC in images [\#277](https://github.com/mintproject/mic/issues/277)
- feat detect parameters in the invocation line [\#202](https://github.com/mintproject/mic/issues/202)

**Merged pull requests:**

- Edit: add mic.log field to bug report template \(\#279\) [\#280](https://github.com/mintproject/mic/pull/280) ([mosoriob](https://github.com/mosoriob))
- Edit: add mic.log field to bug report template [\#279](https://github.com/mintproject/mic/pull/279) ([Cmheidelberg](https://github.com/Cmheidelberg))

## [1.3.0](https://github.com/mintproject/mic/tree/1.3.0) (2020-07-27)

[Full Changelog](https://github.com/mintproject/mic/compare/1.2.1...1.3.0)

**Fixed bugs:**

- MIC is not committing the container [\#265](https://github.com/mintproject/mic/issues/265)
- Error when uploading component [\#260](https://github.com/mintproject/mic/issues/260)
- parameters should be automatically in run.sh [\#254](https://github.com/mintproject/mic/issues/254)

**Closed issues:**

- Track debug info into a log file [\#262](https://github.com/mintproject/mic/issues/262)
- Shorten commands [\#215](https://github.com/mintproject/mic/issues/215)

**Merged pull requests:**

- fix: cleaning code [\#278](https://github.com/mintproject/mic/pull/278) ([mosoriob](https://github.com/mosoriob))
- fix: upload [\#276](https://github.com/mintproject/mic/pull/276) ([mosoriob](https://github.com/mosoriob))
- Develop [\#275](https://github.com/mintproject/mic/pull/275) ([mosoriob](https://github.com/mosoriob))
- F\#266 [\#274](https://github.com/mintproject/mic/pull/274) ([Cmheidelberg](https://github.com/Cmheidelberg))
- F\#266 [\#273](https://github.com/mintproject/mic/pull/273) ([Cmheidelberg](https://github.com/Cmheidelberg))
- Testo [\#272](https://github.com/mintproject/mic/pull/272) ([mosoriob](https://github.com/mosoriob))
- Logging [\#271](https://github.com/mintproject/mic/pull/271) ([Cmheidelberg](https://github.com/Cmheidelberg))
- Develop [\#270](https://github.com/mintproject/mic/pull/270) ([mosoriob](https://github.com/mosoriob))
- System packages [\#269](https://github.com/mintproject/mic/pull/269) ([mosoriob](https://github.com/mosoriob))
- Remove: mic model command [\#259](https://github.com/mintproject/mic/pull/259) ([Cmheidelberg](https://github.com/Cmheidelberg))
- Auto params [\#258](https://github.com/mintproject/mic/pull/258) ([Cmheidelberg](https://github.com/Cmheidelberg))
- F\#215 [\#256](https://github.com/mintproject/mic/pull/256) ([Cmheidelberg](https://github.com/Cmheidelberg))

## [1.2.1](https://github.com/mintproject/mic/tree/1.2.1) (2020-07-21)

[Full Changelog](https://github.com/mintproject/mic/compare/1.2.0...1.2.1)

**Closed issues:**

- Configuration file must be copied into the src directory [\#255](https://github.com/mintproject/mic/issues/255)
- \[Documentation\] Add an estimation of how much time is it required for each step [\#239](https://github.com/mintproject/mic/issues/239)
- Validate directory structure by step [\#130](https://github.com/mintproject/mic/issues/130)

**Merged pull requests:**

- fix\(git\): force push a new repository [\#263](https://github.com/mintproject/mic/pull/263) ([mosoriob](https://github.com/mosoriob))
- F\#203 [\#253](https://github.com/mintproject/mic/pull/253) ([Cmheidelberg](https://github.com/Cmheidelberg))
- Develop [\#251](https://github.com/mintproject/mic/pull/251) ([mosoriob](https://github.com/mosoriob))
- Docker revert [\#250](https://github.com/mintproject/mic/pull/250) ([mosoriob](https://github.com/mosoriob))
-  Docker must run a user on linux [\#248](https://github.com/mintproject/mic/pull/248) ([mosoriob](https://github.com/mosoriob))
- F\#199 [\#245](https://github.com/mintproject/mic/pull/245) ([Cmheidelberg](https://github.com/Cmheidelberg))

## [1.2.0](https://github.com/mintproject/mic/tree/1.2.0) (2020-07-13)

[Full Changelog](https://github.com/mintproject/mic/compare/1.1.1...1.2.0)

**Fixed bugs:**

- allow to upload dt without mc [\#252](https://github.com/mintproject/mic/issues/252)
- Trace not working in docker [\#243](https://github.com/mintproject/mic/issues/243)
- Inputs should be automatically in run.sh [\#203](https://github.com/mintproject/mic/issues/203)
- Docker must run a user on linux [\#142](https://github.com/mintproject/mic/issues/142)

## [1.1.1](https://github.com/mintproject/mic/tree/1.1.1) (2020-07-09)

[Full Changelog](https://github.com/mintproject/mic/compare/1.1.0...1.1.1)

**Merged pull requests:**

- Test trace [\#244](https://github.com/mintproject/mic/pull/244) ([mosoriob](https://github.com/mosoriob))

## [1.1.0](https://github.com/mintproject/mic/tree/1.1.0) (2020-07-09)

[Full Changelog](https://github.com/mintproject/mic/compare/1.0.1...1.1.0)

**Implemented enhancements:**

- Rename `publish` to `upload` [\#231](https://github.com/mintproject/mic/issues/231)

**Closed issues:**

- 1 inputs, 1 outputs and 1 param in cmd [\#185](https://github.com/mintproject/mic/issues/185)

**Merged pull requests:**

- Develop [\#242](https://github.com/mintproject/mic/pull/242) ([mosoriob](https://github.com/mosoriob))
- Docs [\#241](https://github.com/mintproject/mic/pull/241) ([Cmheidelberg](https://github.com/Cmheidelberg))
- Release v1.5.0 [\#237](https://github.com/mintproject/mic/pull/237) ([mosoriob](https://github.com/mosoriob))
- Rename: publish command replaced with upload [\#236](https://github.com/mintproject/mic/pull/236) ([Cmheidelberg](https://github.com/Cmheidelberg))
- fix\(run\_line\): add quotes to string parameter [\#233](https://github.com/mintproject/mic/pull/233) ([mosoriob](https://github.com/mosoriob))

## [1.0.1](https://github.com/mintproject/mic/tree/1.0.1) (2020-07-06)

[Full Changelog](https://github.com/mintproject/mic/compare/1.0.0...1.0.1)

**Implemented enhancements:**

- When publishing, show the URL of the model configuration [\#201](https://github.com/mintproject/mic/issues/201)
- Ease how parameters are declared [\#160](https://github.com/mintproject/mic/issues/160)
- Discussion: What is the best way to ask the parameters? [\#92](https://github.com/mintproject/mic/issues/92)
- mic add autosave [\#84](https://github.com/mintproject/mic/issues/84)
- save in model add command will override without warning [\#82](https://github.com/mintproject/mic/issues/82)
- Improve definitions with examples [\#70](https://github.com/mintproject/mic/issues/70)
- If a model name exists, notify the user [\#69](https://github.com/mintproject/mic/issues/69)
- Add helper functions in MIC to help creating a component [\#61](https://github.com/mintproject/mic/issues/61)
- Simplify some complex resources such as fixed resources [\#46](https://github.com/mintproject/mic/issues/46)
- Adding inputs is cumbersome [\#45](https://github.com/mintproject/mic/issues/45)
- If there are no versions, show a message [\#39](https://github.com/mintproject/mic/issues/39)
- Show doesn't show resources appropriately [\#32](https://github.com/mintproject/mic/issues/32)
- When creating a setup, copy metadata from configuration [\#10](https://github.com/mintproject/mic/issues/10)

**Fixed bugs:**

- gitignore is missing [\#209](https://github.com/mintproject/mic/issues/209)
- \[inputs command\] remove outputs from inputs is not working well [\#208](https://github.com/mintproject/mic/issues/208)
- Step6 crashes if user does not edit Dockerfile [\#151](https://github.com/mintproject/mic/issues/151)
- github push will fail if remote repository is ahead of local  [\#88](https://github.com/mintproject/mic/issues/88)
- Using select on empty Author crashes model add  [\#83](https://github.com/mintproject/mic/issues/83)
- Complex resources do not show definition [\#72](https://github.com/mintproject/mic/issues/72)
- Component and docker image is not available [\#71](https://github.com/mintproject/mic/issues/71)
- Author is registered as "blank node" [\#54](https://github.com/mintproject/mic/issues/54)

**Closed issues:**

- allow to upload datatransformation [\#227](https://github.com/mintproject/mic/issues/227)
- allow define the type of the parameter [\#182](https://github.com/mintproject/mic/issues/182)
- Better outputs for encapsulate steps [\#125](https://github.com/mintproject/mic/issues/125)
- Show metadata completeness levels [\#63](https://github.com/mintproject/mic/issues/63)
- Values get added to main menu instead of sub-menu [\#53](https://github.com/mintproject/mic/issues/53)
- Improve code: add modelconfiguration to model version [\#37](https://github.com/mintproject/mic/issues/37)
- In submenus, "exit" option should be "back" [\#29](https://github.com/mintproject/mic/issues/29)
- allow adding multiple simple resources [\#16](https://github.com/mintproject/mic/issues/16)
- Allow editing existing configurations [\#9](https://github.com/mintproject/mic/issues/9)

**Merged pull requests:**

- Release new version 1.5.0 [\#240](https://github.com/mintproject/mic/pull/240) ([mosoriob](https://github.com/mosoriob))
- Release v1.0.1 [\#232](https://github.com/mintproject/mic/pull/232) ([mosoriob](https://github.com/mosoriob))
- F\#185 [\#230](https://github.com/mintproject/mic/pull/230) ([Cmheidelberg](https://github.com/Cmheidelberg))
- F\#209 [\#229](https://github.com/mintproject/mic/pull/229) ([Cmheidelberg](https://github.com/Cmheidelberg))
- fix: allow to upload a datatransformation [\#228](https://github.com/mintproject/mic/pull/228) ([mosoriob](https://github.com/mosoriob))
- fix: add docker image option [\#226](https://github.com/mintproject/mic/pull/226) ([mosoriob](https://github.com/mosoriob))
- add yaml comments and improve detection of code [\#225](https://github.com/mintproject/mic/pull/225) ([mosoriob](https://github.com/mosoriob))
- \#223  fix: detect binary reprozip inside the default\_path as code\_file [\#224](https://github.com/mintproject/mic/pull/224) ([mosoriob](https://github.com/mosoriob))
- Yaml comments [\#221](https://github.com/mintproject/mic/pull/221) ([Cmheidelberg](https://github.com/Cmheidelberg))

## [1.0.0](https://github.com/mintproject/mic/tree/1.0.0) (2020-06-26)

[Full Changelog](https://github.com/mintproject/mic/compare/0.4.4...1.0.0)

**Implemented enhancements:**

- Automatically detect mic.yaml file in mic/mic.yaml [\#198](https://github.com/mintproject/mic/issues/198)
- Improve Help message [\#179](https://github.com/mintproject/mic/issues/179)
- Add image for Java [\#176](https://github.com/mintproject/mic/issues/176)
- mic encapsulate outputs should support folders [\#167](https://github.com/mintproject/mic/issues/167)
- Improve messages and explanations [\#166](https://github.com/mintproject/mic/issues/166)
- mic encapsulate start is not generic [\#154](https://github.com/mintproject/mic/issues/154)
- \[Documentation\] Update figures [\#136](https://github.com/mintproject/mic/issues/136)
- encapsulate step7 does not remove temporary files [\#124](https://github.com/mintproject/mic/issues/124)
- Format the Docker Output [\#97](https://github.com/mintproject/mic/issues/97)

**Fixed bugs:**

- After publish, DAME command is wrong [\#217](https://github.com/mintproject/mic/issues/217)
- Publish a new version of component fails \(when repository exists\) [\#216](https://github.com/mintproject/mic/issues/216)
- mic run must verify if the outputs have been generated [\#180](https://github.com/mintproject/mic/issues/180)
- add parameter is failing with some values [\#170](https://github.com/mintproject/mic/issues/170)
- \[waiting review} mic encapsulate wrapper fails [\#168](https://github.com/mintproject/mic/issues/168)
- Mic gives all parameters the same position in the KG [\#162](https://github.com/mintproject/mic/issues/162)
- Selecting python3.8 fails [\#159](https://github.com/mintproject/mic/issues/159)
- Wrong text in description when overlapping [\#158](https://github.com/mintproject/mic/issues/158)
- mic encapsulate trace fails [\#157](https://github.com/mintproject/mic/issues/157)
- When I try mic in my docker image \(prepared by mic\) I get an error [\#156](https://github.com/mintproject/mic/issues/156)
- Step6 crash if no inputs [\#139](https://github.com/mintproject/mic/issues/139)
- MIC step does not increase [\#123](https://github.com/mintproject/mic/issues/123)

**Closed issues:**

- java: Simple component with 1 input and output \[S\] [\#192](https://github.com/mintproject/mic/issues/192)
- 1i is a directory [\#191](https://github.com/mintproject/mic/issues/191)
- 1i, 1c, 1o and 1p [\#190](https://github.com/mintproject/mic/issues/190)
- 1i and 1o \(fixed output name\) [\#188](https://github.com/mintproject/mic/issues/188)
- 1i, 1o. output is a directory \(3 files\) [\#187](https://github.com/mintproject/mic/issues/187)
- Test 1:  Component that takes 1 input, 1 output in the invocation line. [\#184](https://github.com/mintproject/mic/issues/184)
- `inputs`: explain what is doing [\#172](https://github.com/mintproject/mic/issues/172)
- Missing documentation in command `inputs` [\#171](https://github.com/mintproject/mic/issues/171)
- \[mic v1\] - step2 Exposing a file inside a directory [\#148](https://github.com/mintproject/mic/issues/148)
- \[mic v1\] - step2 -Write the input and outputs files in the MIC.yaml [\#146](https://github.com/mintproject/mic/issues/146)
- \[mic v1\] - step 2 Find parameters in the commands and write them in the MIC wrapper [\#145](https://github.com/mintproject/mic/issues/145)
- \[mic v1\] - step2 - MIC generates the MIC run file reading the .reprozip/config.yaml [\#144](https://github.com/mintproject/mic/issues/144)
- Improve the message MIC has initialized the component. data/, docker/, src/ and mic.yaml created [\#138](https://github.com/mintproject/mic/issues/138)
- \[mic step3\] - Overview [\#134](https://github.com/mintproject/mic/issues/134)
- \[mic step 2\] overview [\#133](https://github.com/mintproject/mic/issues/133)
- \[mic step1\] Overview [\#131](https://github.com/mintproject/mic/issues/131)
- mic encapsulation needs in depth documentation [\#90](https://github.com/mintproject/mic/issues/90)
- Documentation \[End of June\] [\#68](https://github.com/mintproject/mic/issues/68)

**Merged pull requests:**

- release 1.0.0 [\#222](https://github.com/mintproject/mic/pull/222) ([mosoriob](https://github.com/mosoriob))
- Release v1.0.0 [\#220](https://github.com/mintproject/mic/pull/220) ([mosoriob](https://github.com/mosoriob))
- fix: pull and handle the conflicts [\#218](https://github.com/mintproject/mic/pull/218) ([mosoriob](https://github.com/mosoriob))
- fix: end message publish shows the url to edit it [\#213](https://github.com/mintproject/mic/pull/213) ([mosoriob](https://github.com/mosoriob))
- Yaml comments [\#206](https://github.com/mintproject/mic/pull/206) ([Cmheidelberg](https://github.com/Cmheidelberg))
- Obtain framework safely [\#197](https://github.com/mintproject/mic/pull/197) ([mosoriob](https://github.com/mosoriob))
- Exit and extract python dependencies [\#196](https://github.com/mintproject/mic/pull/196) ([mosoriob](https://github.com/mosoriob))
- Testingv3 [\#195](https://github.com/mintproject/mic/pull/195) ([mosoriob](https://github.com/mosoriob))
- Param detection [\#181](https://github.com/mintproject/mic/pull/181) ([Cmheidelberg](https://github.com/Cmheidelberg))
- Fixing test for issue 168 [\#178](https://github.com/mintproject/mic/pull/178) ([mosoriob](https://github.com/mosoriob))
- Issue 168 [\#169](https://github.com/mintproject/mic/pull/169) ([mosoriob](https://github.com/mosoriob))
- documentation and f139 [\#164](https://github.com/mintproject/mic/pull/164) ([mosoriob](https://github.com/mosoriob))
- Repro zip [\#163](https://github.com/mintproject/mic/pull/163) ([mosoriob](https://github.com/mosoriob))
- Update 01-overview.md [\#153](https://github.com/mintproject/mic/pull/153) ([yolandagil](https://github.com/yolandagil))
- fix: Step6 crash if no inputs \#139  [\#150](https://github.com/mintproject/mic/pull/150) ([mosoriob](https://github.com/mosoriob))
- F\#139 [\#147](https://github.com/mintproject/mic/pull/147) ([Cmheidelberg](https://github.com/Cmheidelberg))
- Add: output log for step6 [\#141](https://github.com/mintproject/mic/pull/141) ([Cmheidelberg](https://github.com/Cmheidelberg))

## [0.4.4](https://github.com/mintproject/mic/tree/0.4.4) (2020-06-08)

[Full Changelog](https://github.com/mintproject/mic/compare/0.4.3...0.4.4)

**Merged pull requests:**

- fix: tests [\#137](https://github.com/mintproject/mic/pull/137) ([mosoriob](https://github.com/mosoriob))

## [0.4.3](https://github.com/mintproject/mic/tree/0.4.3) (2020-06-05)

[Full Changelog](https://github.com/mintproject/mic/compare/0.4.2...0.4.3)

**Implemented enhancements:**

- Detection outputs must ignore model configuration files [\#122](https://github.com/mintproject/mic/issues/122)
- Encapsulation validation [\#94](https://github.com/mintproject/mic/issues/94)
- Validation of Software image [\#59](https://github.com/mintproject/mic/issues/59)

**Fixed bugs:**

- step6 crash if no config field exists in mic.yaml [\#132](https://github.com/mintproject/mic/issues/132)
- If the image build process fails, show a error message [\#121](https://github.com/mintproject/mic/issues/121)

**Closed issues:**

- Step1 should warn users if the directory they  gave alreay exists [\#126](https://github.com/mintproject/mic/issues/126)

**Merged pull requests:**

- fixing small issues [\#129](https://github.com/mintproject/mic/pull/129) ([mosoriob](https://github.com/mosoriob))
- Improved outputs [\#127](https://github.com/mintproject/mic/pull/127) ([Cmheidelberg](https://github.com/Cmheidelberg))

## [0.4.2](https://github.com/mintproject/mic/tree/0.4.2) (2020-06-05)

[Full Changelog](https://github.com/mintproject/mic/compare/0.4.1...0.4.2)

**Implemented enhancements:**

- Test reprozip to help dockerize component [\#89](https://github.com/mintproject/mic/issues/89)
- End-to-end example with model configuration [\#73](https://github.com/mintproject/mic/issues/73)
- New feature: build image [\#66](https://github.com/mintproject/mic/issues/66)
- New feature: validate image [\#60](https://github.com/mintproject/mic/issues/60)
- Guide users when creating test data [\#57](https://github.com/mintproject/mic/issues/57)
- New feature: test model configuration [\#56](https://github.com/mintproject/mic/issues/56)
- New feature: initialize model configuration [\#55](https://github.com/mintproject/mic/issues/55)
- Guide users through issues in the component [\#51](https://github.com/mintproject/mic/issues/51)
- Feature: validate a model configuration [\#50](https://github.com/mintproject/mic/issues/50)

**Fixed bugs:**

- mic step6 error [\#113](https://github.com/mintproject/mic/issues/113)
- encapsulate step2 has missing parameter [\#91](https://github.com/mintproject/mic/issues/91)

**Closed issues:**

- Add docs: extracting dependencies of python [\#116](https://github.com/mintproject/mic/issues/116)
- Improve message step3 [\#115](https://github.com/mintproject/mic/issues/115)
- rename run file to `mic run file` [\#108](https://github.com/mintproject/mic/issues/108)
- rename `mic configuration file` to `mic file` [\#107](https://github.com/mintproject/mic/issues/107)
- rename command mic configure to mic credentials [\#105](https://github.com/mintproject/mic/issues/105)
- Documentation \[End of May\] [\#67](https://github.com/mintproject/mic/issues/67)
- Extend documentation in MIC with guidelines on good component design [\#62](https://github.com/mintproject/mic/issues/62)
- New feature: initialize docker image [\#58](https://github.com/mintproject/mic/issues/58)
- improve the text [\#3](https://github.com/mintproject/mic/issues/3)

**Merged pull requests:**

- Fix: step7 removes temporary files [\#140](https://github.com/mintproject/mic/pull/140) ([Cmheidelberg](https://github.com/Cmheidelberg))
- Improved outputs [\#135](https://github.com/mintproject/mic/pull/135) ([Cmheidelberg](https://github.com/Cmheidelberg))
- Detect dependencies [\#119](https://github.com/mintproject/mic/pull/119) ([mosoriob](https://github.com/mosoriob))
- Develop [\#117](https://github.com/mintproject/mic/pull/117) ([mosoriob](https://github.com/mosoriob))
- F\#107 108 [\#114](https://github.com/mintproject/mic/pull/114) ([Cmheidelberg](https://github.com/Cmheidelberg))
- Add version model [\#110](https://github.com/mintproject/mic/pull/110) ([mosoriob](https://github.com/mosoriob))
- Add version mdodel [\#104](https://github.com/mintproject/mic/pull/104) ([mosoriob](https://github.com/mosoriob))
- Mic ch [\#102](https://github.com/mintproject/mic/pull/102) ([Cmheidelberg](https://github.com/Cmheidelberg))
- Model catalog push [\#100](https://github.com/mintproject/mic/pull/100) ([mosoriob](https://github.com/mosoriob))
- Mic ch [\#99](https://github.com/mintproject/mic/pull/99) ([Cmheidelberg](https://github.com/Cmheidelberg))
- Publish [\#96](https://github.com/mintproject/mic/pull/96) ([mosoriob](https://github.com/mosoriob))
- Mic-ch [\#95](https://github.com/mintproject/mic/pull/95) ([Cmheidelberg](https://github.com/Cmheidelberg))
- Publising [\#87](https://github.com/mintproject/mic/pull/87) ([mosoriob](https://github.com/mosoriob))
- Execution docker + outputs [\#85](https://github.com/mintproject/mic/pull/85) ([mosoriob](https://github.com/mosoriob))
- Step 6 exec [\#81](https://github.com/mintproject/mic/pull/81) ([mosoriob](https://github.com/mosoriob))
- GitHub [\#80](https://github.com/mintproject/mic/pull/80) ([Cmheidelberg](https://github.com/Cmheidelberg))
- Step4: Add the YAML variable in the run [\#79](https://github.com/mintproject/mic/pull/79) ([mosoriob](https://github.com/mosoriob))
- Step 4 create yaml [\#78](https://github.com/mintproject/mic/pull/78) ([mosoriob](https://github.com/mosoriob))
- feat: mic component init [\#76](https://github.com/mintproject/mic/pull/76) ([mosoriob](https://github.com/mosoriob))

## [0.4.1](https://github.com/mintproject/mic/tree/0.4.1) (2020-06-02)

[Full Changelog](https://github.com/mintproject/mic/compare/0.3.0...0.4.1)

**Implemented enhancements:**

- Allow adding a parameter/input/output description [\#103](https://github.com/mintproject/mic/issues/103)

**Closed issues:**

- fix: compatibility between the mic and dame [\#109](https://github.com/mintproject/mic/issues/109)
- rename config.yaml to mic.yaml [\#106](https://github.com/mintproject/mic/issues/106)
- step1 create .gitignore [\#98](https://github.com/mintproject/mic/issues/98)
- mic publish - git [\#77](https://github.com/mintproject/mic/issues/77)

**Merged pull requests:**

- Develop [\#111](https://github.com/mintproject/mic/pull/111) ([mosoriob](https://github.com/mosoriob))

## [0.3.0](https://github.com/mintproject/mic/tree/0.3.0) (2020-05-07)

[Full Changelog](https://github.com/mintproject/mic/compare/0.2.0...0.3.0)

**Implemented enhancements:**

- Metadata validation [\#65](https://github.com/mintproject/mic/issues/65)

**Fixed bugs:**

- Adding a default value in a parameter fails [\#49](https://github.com/mintproject/mic/issues/49)
- Removing options does not remove the functionality [\#48](https://github.com/mintproject/mic/issues/48)

**Closed issues:**

- Enable cancel when the user is editing or adding [\#11](https://github.com/mintproject/mic/issues/11)

**Merged pull requests:**

- fix: reorder structure and align configure with DAME [\#75](https://github.com/mintproject/mic/pull/75) ([mosoriob](https://github.com/mosoriob))
- Fix \#65 [\#74](https://github.com/mintproject/mic/pull/74) ([maurya-rohit](https://github.com/maurya-rohit))
- Fixes Issue \#49 [\#52](https://github.com/mintproject/mic/pull/52) ([dhruvp-8](https://github.com/dhruvp-8))

## [0.2.0](https://github.com/mintproject/mic/tree/0.2.0) (2020-04-16)

[Full Changelog](https://github.com/mintproject/mic/compare/0.1.2...0.2.0)

**Implemented enhancements:**

- Value for 'logo' and 'source' property expects an object, but fails [\#20](https://github.com/mintproject/mic/issues/20)

**Fixed bugs:**

- menu\_select\_property is validating the choice [\#23](https://github.com/mintproject/mic/issues/23)

**Closed issues:**

- Save in some subresources leaves nulls [\#44](https://github.com/mintproject/mic/issues/44)
- Changing the name of an author changes the model name [\#43](https://github.com/mintproject/mic/issues/43)
- Cannot add model configurations [\#42](https://github.com/mintproject/mic/issues/42)
- Adding model configuration from version makes mic crash [\#41](https://github.com/mintproject/mic/issues/41)
- Editing version when "None" makes the program crash [\#40](https://github.com/mintproject/mic/issues/40)
- delete saved.json [\#38](https://github.com/mintproject/mic/issues/38)
- Disable send action in subresource menu [\#33](https://github.com/mintproject/mic/issues/33)
- Define missing fields and classes \(model config, etc.\) [\#7](https://github.com/mintproject/mic/issues/7)

**Merged pull requests:**

- Fixes Issue \#23 and \#33 [\#47](https://github.com/mintproject/mic/pull/47) ([dhruvp-8](https://github.com/dhruvp-8))

## [0.1.2](https://github.com/mintproject/mic/tree/0.1.2) (2020-04-11)

[Full Changelog](https://github.com/mintproject/mic/compare/0.1.1...0.1.2)

## [0.1.1](https://github.com/mintproject/mic/tree/0.1.1) (2020-04-11)

[Full Changelog](https://github.com/mintproject/mic/compare/0.1.0...0.1.1)

## [0.1.0](https://github.com/mintproject/mic/tree/0.1.0) (2020-04-10)

[Full Changelog](https://github.com/mintproject/mic/compare/0.0.4...0.1.0)

**Closed issues:**

- When the user add a configuration, list the versions [\#26](https://github.com/mintproject/mic/issues/26)

**Merged pull requests:**

- Mapping property [\#35](https://github.com/mintproject/mic/pull/35) ([mosoriob](https://github.com/mosoriob))

## [0.0.4](https://github.com/mintproject/mic/tree/0.0.4) (2020-04-10)

[Full Changelog](https://github.com/mintproject/mic/compare/0.0.3...0.0.4)

**Closed issues:**

- When you use the action: `save` in a submenu, the cli tries to save the subresource. [\#31](https://github.com/mintproject/mic/issues/31)
- 'Add' in authors does not work [\#30](https://github.com/mintproject/mic/issues/30)
- Add push [\#28](https://github.com/mintproject/mic/issues/28)
- Wizard saves and exits without asking user [\#27](https://github.com/mintproject/mic/issues/27)
- Add command load from a file [\#25](https://github.com/mintproject/mic/issues/25)
- improve mapping\_resource\_complex [\#24](https://github.com/mintproject/mic/issues/24)
- output json file is not correct [\#22](https://github.com/mintproject/mic/issues/22)
- Remove load option from interactive CLI [\#21](https://github.com/mintproject/mic/issues/21)
- Delete complex resource [\#19](https://github.com/mintproject/mic/issues/19)
- Difference between "add" and "create" is not clear [\#18](https://github.com/mintproject/mic/issues/18)
- Edit in complex object [\#17](https://github.com/mintproject/mic/issues/17)
- readd definition [\#14](https://github.com/mintproject/mic/issues/14)
- show\_choices is showing a lot parameters [\#13](https://github.com/mintproject/mic/issues/13)
- Allow adding multiple complex \(or simple\) objects [\#8](https://github.com/mintproject/mic/issues/8)
- current value is repeating the information of the table [\#6](https://github.com/mintproject/mic/issues/6)
- c to cancel is risky [\#5](https://github.com/mintproject/mic/issues/5)
- Add subresource from a resource [\#4](https://github.com/mintproject/mic/issues/4)
- dont use print use click.echo [\#2](https://github.com/mintproject/mic/issues/2)
- Urgent issues for first release [\#1](https://github.com/mintproject/mic/issues/1)

**Merged pull requests:**

- Add subresources and push [\#34](https://github.com/mintproject/mic/pull/34) ([mosoriob](https://github.com/mosoriob))
- fix: add defintion [\#15](https://github.com/mintproject/mic/pull/15) ([mosoriob](https://github.com/mosoriob))
- feat\(subresource\): allow to select existing resources [\#12](https://github.com/mintproject/mic/pull/12) ([mosoriob](https://github.com/mosoriob))

## [0.0.3](https://github.com/mintproject/mic/tree/0.0.3) (2020-04-03)

[Full Changelog](https://github.com/mintproject/mic/compare/0.0.2...0.0.3)

## [0.0.2](https://github.com/mintproject/mic/tree/0.0.2) (2020-04-03)

[Full Changelog](https://github.com/mintproject/mic/compare/0.0.1...0.0.2)

## [0.0.1](https://github.com/mintproject/mic/tree/0.0.1) (2020-04-03)

[Full Changelog](https://github.com/mintproject/mic/compare/0500f230ecfd65b505ba9597a7e3260bf029e8e7...0.0.1)



\* *This Changelog was automatically generated by [github_changelog_generator](https://github.com/github-changelog-generator/github-changelog-generator)*
