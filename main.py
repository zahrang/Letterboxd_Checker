from scraper import fetch_watchlist_silent
from google_streaming import get_streaming_services  # Switch to Google
from storage import load_watchlist, save_watchlist
from update import compare_watchlists
from config import MY_SERVICES, SERPAPI_KEY, USERNAME, REGION
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.progress import Progress, SpinnerColumn, TextColumn, BarColumn
import time

console = Console()

def main():
    console.clear()
    
    console.print(Panel.fit(
        f"[bold cyan]🎬 Letterboxd Watchlist Checker[/bold cyan]\n[dim]Google Available On API | Region: {REGION.upper()}[/dim]",
        border_style="cyan"
    ))
    console.print()
    
    # Fetch watchlist
    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        console=console,
    ) as progress:
        task = progress.add_task("[cyan]Fetching watchlist...", total=None)
        current_watchlist = fetch_watchlist_silent()
        progress.update(task, completed=True)
    
    if not current_watchlist:
        console.print("\n[red]❌ Could not fetch your watchlist.[/red]")
        return
    
    # Check streaming availability with Google
    available_films = []
    
    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        BarColumn(),
        TextColumn("[progress.percentage]{task.percentage:>3.0f}%"),
        console=console,
    ) as progress:
        task = progress.add_task(
            f"[green]Checking {len(current_watchlist)} films on Google...", 
            total=len(current_watchlist)
        )
        
        for film in current_watchlist:
            services = get_streaming_services(film)
            if services:
                available_films.append((film, services))
            progress.update(task, advance=1)
            time.sleep(0.5)  # Rate limiting
    
    # Show results
    if available_films:
        console.print(f"\n[bold green]✓ Found {len(available_films)} films available on your subscription services![/bold green]\n")
        
        table = Table(title=f"Available in {REGION.upper()} on Your Streaming Services", border_style="green")
        table.add_column("#", style="dim", width=4)
        table.add_column("Film", style="bold white", width=50)
        table.add_column("Services", style="cyan", width=30)
        
        for i, (film, services) in enumerate(available_films, 1):
            table.add_row(str(i), film, " 📺 ".join(services))
        
        console.print(table)
    else:
        console.print("\n[yellow]⚠️ No films found on your subscription services[/yellow]")
        console.print(f"\n[dim]Try:[/dim]")
        console.print(f"  • Verifying your SERPAPI_KEY is valid")
        console.print(f"  • Changing REGION in config.py (try 'US' or 'GB')")
        console.print(f"  • The free tier has 100 searches/month")
    
    console.print()
    console.print(Panel(
        f"[dim]Total: {len(current_watchlist)} films | Available: {len(available_films)} | Region: {REGION.upper()}[/dim]",
        border_style="dim"
    ))


if __name__ == "__main__":
    main()