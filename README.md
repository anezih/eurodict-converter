# kdd2tsv
Convert KoralSoft's EuroDict XP dictionaries to TSV format.
# Usage
`python kdd2tsv.py dictname.KDD`

Script needs pythonnet package and an accompanying dotnet library (RtfPipe) to convert definition body from RTF to HTML. To install pythonnet run:

`pip install pythonnet`

Download RtfPipe nuget from [here](https://www.nuget.org/packages/RtfPipe).

After downloading NuGet package open it as a zip file, copy RtfPipe.dll from `lib > netstandard2.0` and put it right next to this script.

I tested the script with full versions of Turkish⇄French and Turkish⇄Italian dictionaries and some demo versions of (Italian, French, Spanish)-Bulgarian dictionaries. All seems to work fine save for some cyrillic letters, which are displayed broken in Bulgarian definition bodies.

After the conversion, you can convert the TSV file to a format of your choice (for example Kindle MOBI or StarDict) via PyGlossary.
