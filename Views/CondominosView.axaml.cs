using Avalonia.Controls;
using Avalonia.Threading;
using CondominioApp.Data;
using CondominioApp.Models;
using CondominioApp.ViewModels;
using System;

namespace CondominioApp.Views
{
    public partial class CondominosView : Window
    {
        public CondominosView()
        {
            InitializeComponent();

            // 🔧 Força o DataGrid a atualizar depois do carregamento
            this.Opened += async (_, _) =>
            {
                await Dispatcher.UIThread.InvokeAsync(() =>
                {
                    if (DataContext == null)
                    {
                        Console.WriteLine("[DEBUG] DataContext estava nulo — criado manualmente no CondominosView");
                        DataContext = new CondominosViewModel();
                    }

                    // Força refresh
                    if (this.FindControl<DataGrid>("DataGridCondominos") is DataGrid grid)
                    {
                        grid.ItemsSource = ((CondominosViewModel)DataContext).Condominos;
                        grid.InvalidateVisual();
                        Console.WriteLine("[DEBUG] Forçado refresh do DataGrid");
                    }
                });
            };
        }

        private void DataGrid_RowEditEnded(object? sender, DataGridRowEditEndedEventArgs e)
        {
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