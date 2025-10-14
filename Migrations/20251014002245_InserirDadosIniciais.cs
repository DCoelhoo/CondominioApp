using Microsoft.EntityFrameworkCore.Migrations;

#nullable disable

#pragma warning disable CA1814 // Prefer jagged arrays over multidimensional

namespace CondominioApp.Migrations
{
    /// <inheritdoc />
    public partial class InserirDadosIniciais : Migration
    {
        /// <inheritdoc />
        protected override void Up(MigrationBuilder migrationBuilder)
        {
            migrationBuilder.InsertData(
                table: "Condominos",
                columns: new[] { "Id", "Email", "Fracao", "Nome", "Saldo", "Telefone" },
                values: new object[,]
                {
                    { 1, "joao@gmail.com", "A", "João Silva", 150.75m, "912345678" },
                    { 2, "maria@gmail.com", "B", "Maria Costa", -25.00m, "913456789" },
                    { 3, "ricardo@gmail.com", "C", "Ricardo Alves", 0.00m, "914567890" },
                    { 4, "ana@gmail.com", "D", "Ana Pereira", 80.00m, "915678901" },
                    { 5, "pedro@gmail.com", "E", "Pedro Ramos", 20.50m, "916789012" }
                });
        }

        /// <inheritdoc />
        protected override void Down(MigrationBuilder migrationBuilder)
        {
            migrationBuilder.DeleteData(
                table: "Condominos",
                keyColumn: "Id",
                keyValue: 1);

            migrationBuilder.DeleteData(
                table: "Condominos",
                keyColumn: "Id",
                keyValue: 2);

            migrationBuilder.DeleteData(
                table: "Condominos",
                keyColumn: "Id",
                keyValue: 3);

            migrationBuilder.DeleteData(
                table: "Condominos",
                keyColumn: "Id",
                keyValue: 4);

            migrationBuilder.DeleteData(
                table: "Condominos",
                keyColumn: "Id",
                keyValue: 5);
        }
    }
}
