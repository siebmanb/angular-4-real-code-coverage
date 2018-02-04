# Real code coverage in Angular 4

Note: code is not maintained since August 2017

### Introduction
When I started testing Angular 4 code with .spec.ts files, I quickly realized something: even though I was not doing integration tests, my tests were overlapping (see example below). I made it a mission to reach 100% test coverage without overlap. This script allows to find untested code when overlap is disabled.

### Example
Let's have a look at an example.

```ts
<file a.ts>
function A() {
}
```
```ts
<file b.ts>
function B() {
}
```
```ts
<file b.spec.ts>
A()
B()
```
There are two files `a.ts` and `b.ts`, with a spec file `b.spec.ts`. The test file is testing methods from `b.ts` but happens to call methods from `a.ts`.
Oh miracle you end up with 100% coverage on `a.ts` and `b.ts` even though you did not test method `A`!!!

### Solution
The given python script isolates each TS file, run a test coverage by executing only the TS spec file associated with it, and extract the coverage for this TS file only. In other words, the script makes sure a spec file only affect coverage of its associated TS file.

### How to use
Copy the python script in the app root folder and run `python script.py`.

Files containing `fdescribe`,`xdescribe`,`fit` and `xit` will be ignored. 

Results will be in a `results` folder at the root level.

Adjust `hundredPercentCount` to decide when a file is considered as tested. There are 4 counters of cover for each file: statements, branches, functions and lines.

You should probably do as much testing as possible and get close to 100% with the classic code coverage from Angular CLI.

If script fails midway, you might end up with files being modified and not rollbacked. Make sure to cancel the modifications and not commit them.


### Context
Tested with :
  - angular 4.0.3
  - angular CLI 1.0.1
  - typescript 2.2.2
  - jasmine 2.5.2
  - karma 1.2.0
  
### Next step
  - accept a file path as a parameter
  - improve step that removes ../ from stylesheets path
  - accept files with existing `fdescribe`,`xdescribe`,`fit` and `xit`
  
### Disclaimer
This still ain't a real test coverage, because there is no way to know if an executed line has been really tested, but at least there is no more side-effects from other files!

### License
MIT
