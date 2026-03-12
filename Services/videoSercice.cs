using MySql.Data.MySqlClient;

public class VideoService
{
    private string connString = "server=127.0.0.1;user=root;password=;database=nicoflix";

    public async Task<Video?> GetVideoById(int id)
    {
        using var conn = new MySqlConnection(connString);
        await conn.OpenAsync();

        var cmd = new MySqlCommand(
            "SELECT id,file_path,file_name,duration_sec,resolution FROM videos WHERE id=@id",
            conn);

        cmd.Parameters.AddWithValue("@id", id);

        using var reader = await cmd.ExecuteReaderAsync();

        if (await reader.ReadAsync())
        {
            return new Video
            {
                Id = reader.GetInt32("id"),
                FilePath = reader.GetString("file_path"),
                FileName = reader.GetString("file_name"),
                DurationSec = reader.GetInt32("duration_sec"),
                Resolution = reader.GetString("resolution")
            };
        }

        return null;
    }


    /**
    *  Retourne Videos() par catégorie
    */ 
    public async Task<Video?> GetCategorieByCat(int Cat){


            private string connString = "server=127.0.0.1;user=root;password=;database=nicoflix";
        
           using var conn = new MySqlConnection(connString);
        await conn.OpenAsync();

            var cmd = new MySqlCommand(
            "SELECT id,file_path,file_name,duration_sec,resolution FROM videos WHERE category=@Cat",
            conn);

           cmd.Parameters.AddWithValue("@id", id);


            if (await reader.ReadAsync())
        {
            return new Video
            {
                Id = reader.GetInt32("id"),
                FilePath = reader.GetString("file_path"),
                FileName = reader.GetString("file_name"),
                DurationSec = reader.GetInt32("duration_sec"),
                Resolution = reader.GetString("resolution")
            };
        }
    }    

    

}
