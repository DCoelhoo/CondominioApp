using System.Collections.ObjectModel;
using CondominioApp.Models;
using CondominioApp.Data;
using CommunityToolkit.Mvvm.ComponentModel;

namespace CondominioApp.ViewModels
{
    public partial class CondominosViewModel : ObservableObject
    {
        public ObservableCollection<Condomino> Condominos { get; set; }

        public CondominosViewModel()
        {
            using var db = new AppDbContext();
            var lista = db.Condominos.ToList();
            Condominos = new ObservableCollection<Condomino>(lista);
        }
    }
}