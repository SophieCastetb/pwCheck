import argparse
import argparse
import getpass
from pwCheck.strength import evaluate_Password
from pwCheck.breach import check_breach
from pwCheck.generator import generate_password, generate_passphrase

#takes care of pwCheck check by asking for password and rating it
def cmd_check(args):
    #getpass keeps password out of shell history and off screen
    password = getpass.getpass("Enter password: ")

    result = evaluate_Password(password)
    print(f"Rating: {result['rating']}")
    print(f"Entropy: {result['entropy']:.1f}bits")
    for issue in result["issues"]:
        print (f" - {issue}")
    #user asked to skip online check
    if args.no_breach:
        return 0

    breach = check_breach(password)
    if breach["breached"] is None:
        print(f"Breach check skipped: {breach['error']}")
    elif breach["breached"]:
        print(f"WARNING: found in {breach['count'],}known data breachs. Don't use it")
    else:
        print("Not found in known data breaches")

    return 0
#pwCheck generate - prints password or passphrase
def cmd_generate(args):
    try:
        if args.passphrase:
            print(generate_passphrase(args.words, args.separator))
        else:
            print(generate_password(args.length, not args.no_symbols))
    except ValueError as e:
        #bad input
        print(f"Error: {e}")
        return 1
    return 0

#defines commands and options the tool accepts
def build_parser():
    parser= argparse.ArgumentParser(
        prog= "pwCheck",
        description="Check password strength and rbeach exposure, or generate stronger password")
    sub = parser.add_subparsers(dest= "command", required = True)
    #check command
    check = sub.add_parser("check", help= "Check a password's strength and breach status")
    check.add_argument("--no-breach", action = "store_true", help = "Skip the line breach checl")
    check.set_defaults(func=cmd_check)

    #"generate" command
    gen = sub.add_parser("generate", help = "Generate a password or passphrase")
    gen.add_argument("--length", type=int, default=16, help="Password length(default 16)")
    gen.add_argument("--no-symbols", action="store_true", help="Exclude symbols")
    gen.add_argument("--passphrase", action= "store_true", help = "Generatea passphrsae instead")
    gen.add_argument("--words", type=int, default=4, help="Words in passphrase")
    gen.add_argument("--separator", default= "-", help="Passphrase separator(default '-)")
    gen.set_defaults(func=cmd_generate)
    return parser
def main(argv=None):
    args= build_parser().parse_args(argv)
    return args.func(args)
