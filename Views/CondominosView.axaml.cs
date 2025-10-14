using System;
using Avalonia.Controls;
using CondominioApp.Data;
using CondominioApp.Models;

namespace CondominioApp.Views
{
    public partial class CondominosView : Window
    {
        public CondominosView()
        {
            InitializeComponent();
        }

        // Este evento é chamado quando uma linha do DataGrid termina de ser editada
private void DataGrid_RowEditEnded(object? sender, DataGridRowEditEndedEventArgs e)       {
            if (e.Row?.DataContext is Condomino cond)
            {
                try
                {
                    using var db = new AppDbContext();
                    db.Condominos.Update(cond);
                    db.SaveChanges();

                    Console.WriteLine($"Condómino atualizado: {cond.Nome}");
                }
                catch (Exception ex)
                {
                    Console.WriteLine($"Erro ao atualizar condómino {cond.Nome}: {ex.Message}");
                }
            }
        }
    }
}