using System;
using System.Collections.ObjectModel;
using System.Linq;
using CommunityToolkit.Mvvm.ComponentModel;
using CommunityToolkit.Mvvm.Input;
using CondominioApp.Data;
using CondominioApp.Models;

namespace CondominioApp.ViewModels
{
    public partial class CondominosViewModel : ObservableObject
    {
        [ObservableProperty]
        private ObservableCollection<Condomino> condominos;

        [ObservableProperty]
        private Condomino? condominoSelecionado;

        public CondominosViewModel()
        {
            using var db = new AppDbContext();
            Condominos = new ObservableCollection<Condomino>(db.Condominos.ToList());
        }

        [RelayCommand]
        private void AbrirPerfil()
        {
            if (CondominoSelecionado == null)
                return;

            // TODO: Navegar para a página de perfil
            Console.WriteLine($"Abrindo perfil de {CondominoSelecionado.Nome} ({CondominoSelecionado.Fracao})");
        }
    }
}