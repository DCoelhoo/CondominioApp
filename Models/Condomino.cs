using System.ComponentModel.DataAnnotations;
using System.ComponentModel;

namespace CondominioApp.Models;

public class Condomino : INotifyPropertyChanged
{
    [Key]
    public int Id { get; set; }

    private string _nome = "";
    public string Nome
    {
        get => _nome;
        set { _nome = value; OnPropertyChanged(nameof(Nome)); }
    }

    private string _telefone = "";
    public string Telefone
    {
        get => _telefone;
        set { _telefone = value; OnPropertyChanged(nameof(Telefone)); }
    }

    private string _email = "";
    public string Email
    {
        get => _email;
        set { _email = value; OnPropertyChanged(nameof(Email)); }
    }

    private string _fracao = "";
    public string Fracao
    {
        get => _fracao;
        set { _fracao = value; OnPropertyChanged(nameof(Fracao)); }
    }

    private decimal _saldo;
    public decimal Saldo
    {
        get => _saldo;
        set { _saldo = value; OnPropertyChanged(nameof(Saldo)); }
    }

    public event PropertyChangedEventHandler? PropertyChanged;
    protected void OnPropertyChanged(string propertyName) =>
        PropertyChanged?.Invoke(this, new PropertyChangedEventArgs(propertyName));
}