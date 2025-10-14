using Microsoft.EntityFrameworkCore;
using CondominioApp.Models;

namespace CondominioApp.Data
{
    public class AppDbContext : DbContext
    {
        public DbSet<Condomino> Condominos { get; set; }

        protected override void OnConfiguring(DbContextOptionsBuilder optionsBuilder)
        {
            optionsBuilder.UseSqlite("Data Source=Data/condominio.db");
        }

        protected override void OnModelCreating(ModelBuilder modelBuilder)
        {
            // Inserção de dados iniciais (exemplo)
            modelBuilder.Entity<Condomino>().HasData(
                new Condomino { Id = 1, Nome = "João Silva", Fracao = "A", Telefone = "912345678", Email = "joao@gmail.com", Saldo = 150.75m },
                new Condomino { Id = 2, Nome = "Maria Costa", Fracao = "B", Telefone = "913456789", Email = "maria@gmail.com", Saldo = -25.00m },
                new Condomino { Id = 3, Nome = "Ricardo Alves", Fracao = "C", Telefone = "914567890", Email = "ricardo@gmail.com", Saldo = 0.00m },
                new Condomino { Id = 4, Nome = "Ana Pereira", Fracao = "D", Telefone = "915678901", Email = "ana@gmail.com", Saldo = 80.00m },
                new Condomino { Id = 5, Nome = "Pedro Ramos", Fracao = "E", Telefone = "916789012", Email = "pedro@gmail.com", Saldo = 20.50m }
            );
        }
    }
}