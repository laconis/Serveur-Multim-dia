public Regex{
static string NormalizeTimestamp(string input)
    {
        var match = Regex.Match(input, @"^(\d{1,2}):(\d{1,2}):(\d{1,2})$");

        if (!match.Success)
            return null;

        int h = int.Parse(match.Groups[1].Value);
        int m = int.Parse(match.Groups[2].Value);
        int s = int.Parse(match.Groups[3].Value);

        if (h > 23 || m > 59 || s > 59)
            return null;

        return $"{h:D2}:{m:D2}:{s:D2}";
    }

}

