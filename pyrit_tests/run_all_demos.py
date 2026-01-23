"""
PyRIT Master Demo Runner

Run all PyRIT demos sequentially or individually.
"""

import asyncio
import sys
from datetime import datetime


def print_banner(title):
    """Print a formatted banner"""
    print("\n" + "=" * 80)
    print(f"  {title}")
    print("=" * 80 + "\n")


async def run_demo(demo_name, demo_func):
    """Run a single demo with error handling"""
    print_banner(f"Starting: {demo_name}")
    
    try:
        await demo_func()
        print(f"\n✅ {demo_name} completed successfully")
        return True
    except Exception as e:
        print(f"\n❌ {demo_name} failed: {e}")
        import traceback
        traceback.print_exc()
        return False


async def run_all_demos():
    """Run all demos in sequence"""
    
    start_time = datetime.now()
    
    print_banner("PyRIT Comprehensive Demo Suite")
    print("This will run all 5 PyRIT demos:")
    print("  1. Basic Prompt Sending with Converters")
    print("  2. Crescendo Multi-Turn Attacks")
    print("  3. Scoring and Evaluation")
    print("  4. Multi-Modal Attacks")
    print("  5. Memory and Analysis")
    print()
    print("⏱️  Estimated time: 10-20 minutes")
    print()
    input("Press Enter to continue or Ctrl+C to cancel...")
    
    results = {}
    
    # Demo 1: Basic Attacks
    print("\n" + "🔹" * 40)
    print("DEMO 1/5: Basic Prompt Sending")
    print("🔹" * 40)
    
    try:
        from pyrit_tests import demo_01_basic as demo1
        results['Basic Attacks'] = await run_demo(
            "Demo 1: Basic Prompt Sending",
            demo1.run_basic_attacks
        )
    except ImportError:
        # Run as script
        import subprocess
        result = subprocess.run([sys.executable, "01_basic_prompt_sending.py"])
        results['Basic Attacks'] = result.returncode == 0
    
    # Demo 2: Crescendo
    print("\n" + "🔹" * 40)
    print("DEMO 2/5: Crescendo Multi-Turn Attacks")
    print("🔹" * 40)
    print("⚠️  This demo can take 5-10 minutes per attack")
    
    try:
        from pyrit_tests import demo_02_crescendo as demo2
        results['Crescendo Attacks'] = await run_demo(
            "Demo 2: Crescendo Attack",
            demo2.run_all_crescendo_attacks
        )
    except ImportError:
        result = subprocess.run([sys.executable, "02_crescendo_attack.py"])
        results['Crescendo Attacks'] = result.returncode == 0
    
    # Demo 3: Scoring
    print("\n" + "🔹" * 40)
    print("DEMO 3/5: Scoring and Evaluation")
    print("🔹" * 40)
    
    try:
        from pyrit_tests import demo_03_scoring as demo3
        results['Scoring'] = await run_demo(
            "Demo 3: Scoring",
            demo3.demonstrate_scale_scorers
        )
    except ImportError:
        result = subprocess.run([sys.executable, "03_scoring_evaluation.py"])
        results['Scoring'] = result.returncode == 0
    
    # Demo 4: Multi-Modal
    print("\n" + "🔹" * 40)
    print("DEMO 4/5: Multi-Modal Attacks")
    print("🔹" * 40)
    
    try:
        from pyrit_tests import demo_04_multimodal as demo4
        results['Multi-Modal'] = await run_demo(
            "Demo 4: Multi-Modal",
            demo4.run_qr_code_attack
        )
    except ImportError:
        result = subprocess.run([sys.executable, "04_qr_code_attacks.py"])
        results['Multi-Modal'] = result.returncode == 0
    
    # Demo 5: Memory
    print("\n" + "🔹" * 40)
    print("DEMO 5/5: Memory and Analysis")
    print("🔹" * 40)
    
    try:
        from pyrit_tests import demo_05_memory as demo5
        results['Memory Analysis'] = await run_demo(
            "Demo 5: Memory",
            demo5.demonstrate_memory_persistence
        )
    except ImportError:
        result = subprocess.run([sys.executable, "05_memory_analysis.py"])
        results['Memory Analysis'] = result.returncode == 0
    
    # Final Summary
    end_time = datetime.now()
    duration = end_time - start_time
    
    print_banner("FINAL SUMMARY")
    print(f"Total execution time: {duration}")
    print()
    print("Results:")
    
    success_count = 0
    for demo_name, success in results.items():
        status = "✅ PASSED" if success else "❌ FAILED"
        print(f"  {status}: {demo_name}")
        if success:
            success_count += 1
    
    print()
    print(f"Success rate: {success_count}/{len(results)} demos passed")
    
    if success_count == len(results):
        print("\n🎉 All demos completed successfully!")
    else:
        print(f"\n⚠️  {len(results) - success_count} demo(s) failed")
    
    print()
    print("💾 Check ~/.pyrit/results/ for stored data")
    print("📊 Run 05_memory_analysis.py to analyze results")
    print()


def show_menu():
    """Show interactive menu"""
    print_banner("PyRIT Demo Suite - Interactive Menu")
    
    print("Choose an option:")
    print()
    print("  [1] Run all demos (10-20 minutes)")
    print("  [2] Demo 1: Basic Prompt Sending (2-3 minutes)")
    print("  [3] Demo 2: Crescendo Attacks (10-15 minutes)")
    print("  [4] Demo 3: Scoring & Evaluation (3-5 minutes)")
    print("  [5] Demo 4: Multi-Modal Attacks (2-3 minutes)")
    print("  [6] Demo 5: Memory & Analysis (1-2 minutes)")
    print("  [q] Quit")
    print()
    
    choice = input("Enter your choice: ").strip().lower()
    return choice


async def run_single_demo(demo_number):
    """Run a single demo by number"""
    import subprocess
    
    demos = {
        '2': ('01_basic_prompt_sending.py', 'Basic Prompt Sending'),
        '3': ('02_crescendo_attack.py', 'Crescendo Multi-Turn Attacks'),
        '4': ('03_scoring_evaluation.py', 'Scoring & Evaluation'),
        '5': ('04_qr_code_attacks.py', 'QR Code Attacks'),
        '6': ('05_memory_analysis.py', 'Memory & Analysis'),
    }
    
    if demo_number in demos:
        script, name = demos[demo_number]
        print_banner(f"Running: {name}")
        result = subprocess.run([sys.executable, script])
        
        if result.returncode == 0:
            print(f"\n✅ {name} completed!")
        else:
            print(f"\n❌ {name} failed!")
    else:
        print("Invalid choice")


def main():
    """Main entry point"""
    
    if len(sys.argv) > 1:
        # Command line argument
        arg = sys.argv[1].lower()
        
        if arg in ['--all', '-a']:
            print("Running all demos...")
            asyncio.run(run_all_demos())
        elif arg in ['--help', '-h']:
            print("PyRIT Demo Runner")
            print()
            print("Usage:")
            print("  python run_all_demos.py          # Interactive menu")
            print("  python run_all_demos.py --all    # Run all demos")
            print("  python run_all_demos.py --help   # Show this help")
        else:
            print(f"Unknown argument: {arg}")
            print("Use --help for usage information")
    else:
        # Interactive menu
        while True:
            choice = show_menu()
            
            if choice == 'q':
                print("Goodbye!")
                break
            elif choice == '1':
                asyncio.run(run_all_demos())
                break
            elif choice in ['2', '3', '4', '5', '6']:
                asyncio.run(run_single_demo(choice))
                print("\n" + "=" * 80)
                input("\nPress Enter to return to menu...")
            else:
                print("\n❌ Invalid choice. Please try again.\n")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n👋 Interrupted by user")
        sys.exit(0)
