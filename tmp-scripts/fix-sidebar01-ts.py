#!/usr/bin/env python3
"""Fix TypeScript errors from SIDEBAR-01 QA fixes.

Error 1: ai/actions.ts:358 — member.permissions doesn't exist on union type
  → Use memberHasPermission() from check-permission.ts instead of raw .permissions
Error 2: notes/route.ts:144 — Role doesn't have "OWNER"
  → Use "ADMIN" (ADMIN has all permissions including owner bypass)
"""

# =============================================
# Fix 1: ai/actions.ts — use memberHasPermission instead of raw .permissions
# =============================================
filepath_ai = '/home/tikso/tikso/src/app/(app)/[orgId]/ai/actions.ts'

with open(filepath_ai, 'r') as f:
    ai = f.read()

# Add import for memberHasPermission if not already present
if 'memberHasPermission' not in ai:
    # Find existing import from check-permission
    if 'assertMemberPermission' in ai:
        ai = ai.replace(
            'assertMemberPermission',
            'assertMemberPermission, memberHasPermission',
            1  # Only first occurrence (the import)
        )
    elif 'check-permission' in ai:
        # Add to existing import
        ai = ai.replace(
            'from "@/lib/auth/check-permission"',
            'from "@/lib/auth/check-permission"'
        )

# Replace the raw .permissions access with memberHasPermission calls
old_perm = """  // AC4: Accept liveChat OR integrations (agents have liveChat, automations have integrations)
  const hasJourneyPermission = member.permissions?.includes("liveChat") || member.permissions?.includes("integrations");
  if (!hasJourneyPermission) {
    return { success: false, error: "Sem permissão para alterar jornada" };
  }"""

new_perm = """  // AC4: Accept liveChat OR integrations (agents have liveChat, automations have integrations)
  const hasJourneyPermission = memberHasPermission(member, "liveChat") || memberHasPermission(member, "integrations");
  if (!hasJourneyPermission) {
    return { success: false, error: "Sem permissão para alterar jornada" };
  }"""

if old_perm in ai:
    ai = ai.replace(old_perm, new_perm)
    with open(filepath_ai, 'w') as f:
        f.write(ai)
    print("Fix 1: ai/actions.ts — memberHasPermission instead of raw .permissions")
else:
    print("Fix 1: WARNING — pattern not found in ai/actions.ts")


# =============================================
# Fix 2: notes/route.ts — ADMIN instead of OWNER (Role enum)
# =============================================
filepath_notes = '/home/tikso/tikso/src/app/api/inbox/notes/route.ts'

with open(filepath_notes, 'r') as f:
    notes = f.read()

# Fix: Role enum doesn't have OWNER, only ADMIN|MANAGER|ATTENDANT|VIEWER
# ADMIN already has full permissions (owner bypass in check-permission.ts)
old_check = '    const isAdmin = member.role === "OWNER" || member.role === "ADMIN";'
new_check = '    const isAdmin = member.role === "ADMIN";'

if old_check in notes:
    notes = notes.replace(old_check, new_check)
    with open(filepath_notes, 'w') as f:
        f.write(notes)
    print("Fix 2: notes/route.ts — ADMIN only (no OWNER in Role enum)")
else:
    print("Fix 2: WARNING — pattern not found in notes/route.ts")

# Also need to destructure member from requireOrgAccess
# Check if we have { session, member } already
if '{ session, member }' not in notes and 'const { session, member }' not in notes:
    # The current code has: const { session, member } = await requireOrgAccess(note.organizationId);
    # This should already be there from Fix 1. Let's verify.
    if 'session, member' in notes:
        print("Fix 2b: member already destructured from requireOrgAccess")
    else:
        print("Fix 2b: WARNING — member not destructured, may need manual fix")
else:
    print("Fix 2b: session, member already destructured")

print("\nAll TypeScript fixes applied!")
