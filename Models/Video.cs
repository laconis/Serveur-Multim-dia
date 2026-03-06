using System.ComponentModel.DataAnnotations;
using System.ComponentModel.DataAnnotations.Schema;

namespace Newtube.Models
{
    public class Video
    {
        public int Id { get; set; }

        [Required]
        [MaxLength(255)]
        public string Title { get; set; } = string.Empty;

        [MaxLength(2000)]
        public string? Description { get; set; }

        [Required]
        [MaxLength(500)]
        public string FilePath { get; set; } = string.Empty;

        [Required]
        [MaxLength(255)]
        public string FileName { get; set; } = string.Empty;

        [MaxLength(64)]
        public string? HashSha256 { get; set; }

        [MaxLength(500)]
        public string? CoverPath { get; set; }

        public long SizeBytes { get; set; }

        public int DurationSec { get; set; }

        [MaxLength(50)]
        public string? Resolution { get; set; }

        public DateTime CreatedAt { get; set; } = DateTime.Now;

        public DateTime? UpdatedAt { get; set; }

        public bool IsPublished { get; set; } = true;

        public bool IsDeleted { get; set; } = false;

        public long Views { get; set; } = 0;

        // Clé étrangère catégorie
        public int CategoryId { get; set; }
        public Category? Category { get; set; }

        // Optionnel : utilisateur qui a uploadé
        [MaxLength(100)]
        public string? UploadedBy { get; set; }

        [NotMapped]
        public string DurationFormatted
        {
            get
            {
                return TimeSpan.FromSeconds(DurationSec).ToString(@"hh\:mm\:ss");
            }
        }

        [NotMapped]
        public string SizeFormatted
        {
            get
            {
                if (SizeBytes < 1024)
                    return $"{SizeBytes} B";

                if (SizeBytes < 1024 * 1024)
                    return $"{SizeBytes / 1024.0:F2} KB";

                if (SizeBytes < 1024 * 1024 * 1024)
                    return $"{SizeBytes / 1024.0 / 1024.0:F2} MB";

                return $"{SizeBytes / 1024.0 / 1024.0 / 1024.0:F2} GB";
            }
        }
    }
}
